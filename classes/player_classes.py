import random

class Player:
    def __init__(self, name, is_human=True):
        self.name = name
        self.is_human = is_human
        self.star_cards = []
        self.hand = []
        self.location = []
        self.attached_fans = []


    def play_star(self, card):
        """
        Play a StarCard from hand to the board.
        """
        self.hand.remove(card)
        self.star_cards.append(card)
        print(f"{self.name} plays {card.name}")

    def play_star_from_hand(self):
        if not self.hand:
            print(f"{self.name} has no cards in hand to play.")
            return
        self.play_star(self.hand[0])

    def choose_star_for_contest(self):
        """
        Default behavior: return the most recently played star.
        Override in subclasses.
        """
        return self.star_cards[-1] if self.star_cards else None
    
    @property
    def fans(self):
        total = 0
        for star in self.star_cards:
            for fan in getattr(star, "attached_fans", []):
                bonus = fan.bonus
                if fan.condition_tag and fan.applies_to(star):
                    bonus += 1  # bonus fan match
                total += bonus
        return total

    def __str__(self):
        return f"{self.name} | Stars: {[s.name for s in self.star_cards]} | Fans: {self.fans}"


class HumanPlayer(Player):

    def play_star_from_hand(self):
        if not self.hand:
            print("You have no cards to play.")
            return

        while True:
            choice = input("Choose a card to play (or press Enter to skip): ")
            if choice == "":
                print(f"{self.name} chose to skip playing a card.")
                return
            if choice.isdigit():
                idx = int(choice)
                if 0 <= idx < len(self.hand):
                    chosen = self.hand[idx]
                    self.play_star(chosen)
                    return
            print("Invalid choice. Try again.")

    def choose_star_for_contest(self):
        if not self.star_cards:
            return None

        while True:
            choice = input(f"{self.name}, choose a star for the contest (0-{len(self.star_cards)-1}): ")
            if choice.isdigit():
                idx = int(choice)
                if 0 <= idx < len(self.star_cards):
                    return self.star_cards[idx]
            print("Invalid choice, try again.")


class ComputerPlayer(Player):

    def __init__(self, name):
        super().__init__(name, is_human=False)

    def play_star_from_hand(self):
        if not self.hand:
            return
        card = random.choice(self.hand)
        self.play_star(card)  # this will remove it inside
            
    def choose_star_for_contest(self):
        if not self.star_cards:
            return None
        chosen = random.choice(self.star_cards)
        print(f"{self.name} chooses {chosen.name} for the contest.")
        return chosen
