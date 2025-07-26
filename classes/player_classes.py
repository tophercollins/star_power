import random
from utils.display_utils import display_card_list

class Player:
    def __init__(self, name):
        self.name = name
        self.played_stars = []
        self.fans = 0  # Replace with a list of FanCards later if needed
        self.hand = []  # in Player.__init__()

    def play_star(self, card):
        """
        Play a StarCard from hand to the board.
        """
        self.hand.remove(card)
        self.played_stars.append(card)
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
        return self.played_stars[-1] if self.played_stars else None

    def __str__(self):
        return f"{self.name} | Stars: {[s.name for s in self.played_stars]} | Fans: {self.fans}"


class HumanPlayer(Player):

    def play_star_from_hand(self):
        if not self.hand:
            print("You have no cards to play.")
            return

        print("\n🖐️ Your hand:")
        display_card_list(self.hand, title="🖐️ Your Hand")      
        """for i, card in enumerate(self.hand):
            print(f"{i}: {card}")"""

        while True:
            choice = input("Choose a card to play (or press Enter to skip): ")
            if choice == "":
                print("You chose to skip playing a card.")
                return
            if choice.isdigit():
                idx = int(choice)
                if 0 <= idx < len(self.hand):
                    chosen = self.hand[idx]
                    self.play_star(chosen)
                    return
            print("Invalid choice. Try again.")

    def choose_star_for_contest(self):
        if not self.played_stars:
            return None

        print("\nYour played stars:")
        display_card_list(self.played_stars, title="Your Stars in Play")

        while True:
            choice = input(f"{self.name}, choose a star for the contest (0-{len(self.played_stars)-1}): ")
            if choice.isdigit():
                idx = int(choice)
                if 0 <= idx < len(self.played_stars):
                    return self.played_stars[idx]
            print("Invalid choice, try again.")


class ComputerPlayer(Player):

    def play_star_from_hand(self):
        if not self.hand:
            return
        card = random.choice(self.hand)
        self.play_star(card)  # this will remove it inside
            
    def choose_star_for_contest(self):
        if not self.played_stars:
            return None
        chosen = random.choice(self.played_stars)
        print(f"{self.name} chooses {chosen.name} for the contest.")
        return chosen
