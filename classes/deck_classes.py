import random

class Deck:
    def __init__(self, cards=None):
        self.cards = cards[:] if cards else []
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop(0) if self.cards else None

    def add(self, card):
        self.cards.append(card)

    def add_many(self, cards):
        self.cards.extend(cards)

    def peek(self, n=1):
        return self.cards[:n]

    def count(self):
        return len(self.cards)

    def is_empty(self):
        return len(self.cards) == 0