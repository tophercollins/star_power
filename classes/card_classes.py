import random

# Star Cards
class StarCard:
    def __init__(self, name, aura, talent, influence, legacy, tags=[]):
        """
        tags: Optional list like ['rapper', 'pop star']
        """
        self.name = name
        self.aura = aura
        self.talent = talent
        self.influence = influence
        self.legacy = legacy
        self.tags = tags
        self.attached_fans = []
        self.attached_power_cards = []

    def __str__(self):
        tag_str = f" ({', '.join(self.tags)})" if self.tags else ""
        return (
            f"{self.name}{tag_str} | "
            f"Aura: {self.aura}, Talent: {self.talent}, "
            f"Influence: {self.influence}, Legacy: {self.legacy}"
        )

    def get_stat(self, stat_name):
        base = getattr(self, stat_name, 0)
        modifiers = sum(
            pc.get_stat_modifier(stat_name)
            for pc in self.attached_power_cards
            if hasattr(pc, 'get_stat_modifier')
        )
        return max(0, base + modifiers)

    def get_fan_bonus(self):
        fan_bonus = 0
        for fan in self.attached_fans:
            fan_bonus += fan.bonus
            if fan.tag in self.tags:
                fan_bonus += 1
        return fan_bonus

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
        if self.type == "fixed":
            stat = self.stat_options[0]
        else:
            if not chosen_stat:
                raise ValueError("Must provide a stat choice for this event.")
            stat = chosen_stat

        max_value = max(star.get_stat(stat) for star in stars)
        winners = [star for star in stars if star.get_stat(stat) == max_value]

        return winners


class FanCard:
    def __init__(self, name, bonus, tag=None):
        self.name = name
        self.bonus = bonus
        self.tag = tag

    def __str__(self):
        if self.tag:
            return f"{self.name} (+{self.bonus}) Gives an extra +1 if star is a {self.condition_tag}"
        else:
            return f"{self.name} (+{self.bonus})"

# Power Cards
class PowerCard:
    def __init__(self, name, description="", targets_star=False):
        self.name = name
        self.description = description or "No description provided."
        self.targets_star = targets_star

    def play(self, player, game):
        """
        Execute the effect of this power card.
        Must be implemented by subclasses.
        """
        raise NotImplementedError("play() must be implemented by subclasses")

    def __str__(self):
        return f"{self.name} - {self.description}"

class ModifyStatCard(PowerCard):
    def __init__(self, name, stat_modifiers: dict, description=None):
        self.stat_modifiers = {k: v for k, v in stat_modifiers.items() if v != 0}
        self.targets_star = True
        desc = description or self._build_description()
        super().__init__(name, desc)

    def _build_description(self):
        return ", ".join([f"{k.capitalize()} {v:+d}" for k, v in self.stat_modifiers.items()]) + " (attach to Star)"

    def get_stat_modifier(self, stat_name):
        return self.stat_modifiers.get(stat_name, 0)

    def play(self, player, game):
        valid_targets = player.played_stars
        if not valid_targets:
            print("No valid Stars to attach this card to.")
            return

        # Human or AI choose star
        if player.is_human:
            print(f"\nChoose a Star to attach {self.name} to:")
            for i, star in enumerate(valid_targets):
                print(f"{i}: {star}")
            while True:
                try:
                    choice = int(input("Enter the number of the Star: "))
                    if 0 <= choice < len(valid_targets):
                        target_star = valid_targets[choice]
                        break
                except ValueError:
                    print("Invalid input.")
        else:
            target_star = random.choice(valid_targets)

        target_star.attached_power_cards.append(self)
        player.hand.remove(self)
        print(f"{self.name} attached to {target_star.name}.")


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
