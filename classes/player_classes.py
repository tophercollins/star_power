import random

class Player:
    def __init__(self, name, is_human=True):
        self.name = name
        self.is_human = is_human
        self.hand = []
        self.star_cards = []
        self.locations = []

    def choose(self, options, prompt, allow_skip):
        if self.is_human:
            return self.human_choose(options, prompt, allow_skip)
        else:
            return self.ai_choose(options)


    def human_choose(self, options, prompt="Choose an option:", allow_skip=False):
        """
        Allow human players to choose an option (a star, a stat, etc.)
        options: list of option names or objects
        prompt: message to display for choice
        """
        if not options:
            print("No options available.")
            return None
        while True:
            print(prompt)
            for i, option in enumerate(options):
                print(f"{i}: {option}")
            if allow_skip:
                print("Press Enter to skip")
            choice = input("Enter the number of your choice: ").strip()
            if choice == "" and allow_skip:
                return None
            if choice.isdigit():
                idx = int(choice)
                if 0 <= idx < len(options):
                    return options[idx]
            print("Invalid choice. Try again.")

    def ai_choose(self, options):
        """
        AI chooses an option randomly from the available options.
        """
        if not options:
            return None
        return random.choice(options)

    def play_card(self, card, target):
        """
        Play a card from hand to given target.
        Example:
        - Play a star card to the board - self.play_card(card, self.star_cards)
        - Play a location card to the board - self.play_card(card, self.locations)
        - Attach a power card to a star - self.play_card(card, star.attached_power_cards)
        """
        self.hand.remove(card)
        target.append(card)
        print(f"{self.name} plays {card.name}")

    def __str__(self):
        return f"{self.name} | Stars: {[s.name for s in self.star_cards]} | Locations: {[l.name for l in self.locations]}"