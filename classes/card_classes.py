import random

# Star Cards
class StarCard:
    def __init__(self, name, aura, talent, influence, legacy, tags=None):
        """
        tags: Optional list like ['rapper', 'pop star']
        """
        self.name = name
        self.aura = aura
        self.talent = talent
        self.influence = influence
        self.legacy = legacy
        self.tags = tags or []
        self.attached_fans = []  # List of FanCard objects

    def __str__(self):
        tag_str = f" ({', '.join(self.tags)})" if self.tags else ""
        return (
            f"{self.name}{tag_str} | "
            f"Aura: {self.aura}, Talent: {self.talent}, "
            f"Influence: {self.influence}, Legacy: {self.legacy}"
        )

    def get_stat(self, stat_name):
        return getattr(self, stat_name, None)

# Event Cards
class EventCard:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description

    def resolve(self, stars):
        """
        Should be implemented by child classes.
        stars: list of StarCard instances.
        """
        raise NotImplementedError("resolve() must be implemented by subclasses")

    def __str__(self):
        return f"{self.name} - {self.description}"

class StatContestEvent(EventCard):
    def __init__(self, name, stat_options, description=None):
        """
        stat_options: list of allowed stats for this contest
        """
        self.stat_options = [s.lower() for s in stat_options]

        # Auto-determine contest type
        if len(self.stat_options) == 1:
            self.type = "fixed"
        elif len(self.stat_options) == 2:
            self.type = "choice_of_2"
        elif len(self.stat_options) == 4:
            self.type = "choice_of_4"
        else:
            self.type = "custom"

        desc = description or self._default_description()
        super().__init__(name, desc)

    def _default_description(self):
        if self.type == "fixed":
            return f"Contest based on {self.stat_options[0].capitalize()}"
        else:
            options = " / ".join(s.capitalize() for s in self.stat_options)
            return f"Choose one stat to compete in: {options}"

    def resolve(self, stars, chosen_stat=None):
        """
        stars: list of StarCard objects
        chosen_stat: required if event type allows choice
        """
        if not self.stat_options:
            raise ValueError("No stats defined for contest.")

        if self.type == "fixed":
            stat = self.stat_options[0]
        else:
            if not chosen_stat:
                raise ValueError("Must provide a stat choice for this event.")
            if chosen_stat.lower() not in self.stat_options:
                raise ValueError(f"{chosen_stat} is not a valid stat for this contest.")
            stat = chosen_stat.lower()

        max_value = max(star.get_stat(stat) for star in stars)
        winners = [star for star in stars if star.get_stat(stat) == max_value]

        if len(winners) > 1 and game:
            for player in game.players:
                for location in player.locations:
                    if location.overrides_tie():
                        for winner in winners:
                            if winner in player.played_stars:
                                return [winner]  # Player with tie-break location wins
        return winners


class FanCard:
    def __init__(self, name, bonus, condition_tag=None, description=None):
        self.name = name
        self.bonus = bonus
        self.condition_tag = condition_tag.lower() if condition_tag else None
        self.description = description or self._generate_description()

    def _generate_description(self):
        if self.condition_tag:
            article = "an" if self.condition_tag[0].lower() in "aeiou" else "a"
            return f"Gives +1 if star is {article} {self.condition_tag.title()}"
        return "Unconditional fan bonus"

    def applies_to(self, star_card):
        if not self.condition_tag:
            return True
        return self.condition_tag in [t.lower() for t in star_card.tags]

    def __str__(self):
        return f"{self.name} (+{self.bonus}) - {self.description}"



# Power Cards
class PowerCard:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description or "No description provided."

    def play(self, player, game):
        """
        Execute the effect of this power card.
        Must be implemented by subclasses.
        """
        raise NotImplementedError("play() must be implemented by subclasses")

    def __str__(self):
        return f"{self.name} - {self.description}"

class DrawCards(PowerCard):
    def __init__(self, name, num_to_draw, num_to_discard=0, description=None, discard_strategy=None):
        self.num_to_draw = num_to_draw
        self.num_to_discard = num_to_discard
        self.discard_strategy = discard_strategy

        desc = description or f"Draw {num_to_draw} card(s)" + (f", then discard {num_to_discard}" if num_to_discard else "")
        super().__init__(name=name, description=desc)

    def play(self, player, game):
        drawn = []
        for _ in range(self.num_to_draw):
            card = game.main_deck.draw()
            if card:
                player.hand.append(card)
                drawn.append(card)
                print(f"{player.name} drew a card: {card}")
            else:
                print("Deck is empty. No more cards to draw.")
                break

        if self.num_to_discard > 0:
            if self.discard_strategy:
                cards_to_discard = self.discard_strategy(player)
            elif getattr(player, 'is_human', False):  # Human player input
                cards_to_discard = self.prompt_human_discard(player)
            else:
                # Fallback for AI: discard first N cards
                cards_to_discard = player.hand[:self.num_to_discard]

            for card in cards_to_discard:
                if card in player.hand:
                    player.hand.remove(card)
                    game.discard_pile.append(card)
                    print(f"{player.name} discarded: {card}")

        return drawn

    def prompt_human_discard(self, player):
        print(f"\n{player.name}, choose {self.num_to_discard} card(s) to discard from your hand:")
        for i, card in enumerate(player.hand):
            print(f"{i}: {card}")
        indices = []
        while len(indices) < self.num_to_discard:
            try:
                choice = int(input(f"Select card #{len(indices)+1}: "))
                if 0 <= choice < len(player.hand) and choice not in indices:
                    indices.append(choice)
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Please enter a number.")
        return [player.hand[i] for i in indices]

class ModifyStatCard(PowerCard):
    def __init__(self, name, stat, amount, target_self=True, target_opponent=True, description=None):
        """
        stat: which stat to modify (e.g. "aura")
        amount: positive or negative integer
        target_self: can this be used on your own stars?
        target_opponent: can this be used on opponent's stars?
        """
        self.stat = stat.lower()
        self.amount = amount
        self.target_self = target_self
        self.target_opponent = target_opponent

        sign = "+" if amount > 0 else ""
        desc = description or f"{sign}{amount} {stat.capitalize()} to a target star"
        super().__init__(name=name, description=desc)

    def play(self, player, game):
        # Determine eligible targets
        targets = []
        if self.target_self:
            targets += [(player, star) for star in player.played_stars]
        if self.target_opponent:
            for p in game.players:
                if p != player:
                    targets += [(p, star) for star in p.played_stars]

        if not targets:
            print("No valid targets for this power card.")
            return

        # Let human choose; AI will choose randomly
        if player.is_human:
            print(f"\nChoose a target star to modify {self.stat.capitalize()} by {self.amount}:")
            for i, (_, star) in enumerate(targets):
                print(f"{i}: {star}")
            while True:
                choice = input("Enter the number of the star to target: ")
                if choice.isdigit():
                    idx = int(choice)
                    if 0 <= idx < len(targets):
                        _, target_star = targets[idx]
                        break
                print("Invalid choice.")
        else:
            _, target_star = random.choice(targets)
            print(f"{player.name} uses {self.name} on {target_star.name}")

        # Apply stat change
        current_value = target_star.get_stat(self.stat)
        new_value = max(0, current_value + self.amount)  # Clamp at 0
        setattr(target_star, self.stat, new_value)
        print(f"{target_star.name}'s {self.stat.capitalize()} is now {new_value}")

class LocationPowerCard(PowerCard):
    def __init__(self, name, description):
        super().__init__(name=name, description=description)

    def apply_effect(self, player, game):
        """
        Called each round or on relevant trigger.
        Should be overridden by subclasses.
        """
        raise NotImplementedError("LocationPowerCard must implement apply_effect.")

    def modify_star(self, star, context=None):
        """
        Optional hook to modify star stats passively.
        Can return a dict of stat modifiers, e.g. {"aura": +1}
        """
        return {}

    def overrides_tie(self):
        """
        Returns True if this location causes the player to win ties.
        Default: False
        """
        return False
