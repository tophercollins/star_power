import random
import json
from classes.card_classes import StarCard, StatContestEvent
from resources.config import GAME_CONFIG

class Deck:
    def __init__(self, cards=None):
        """
        cards: Optional list of initial cards
        """
        self.cards = cards[:] if cards else []
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        if self.cards:
            return self.cards.pop(0)
        return None  # Deck is empty

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


class MainDeck(Deck):
    def __init__(self, json_path="resources/starcards.json", total_cards=GAME_CONFIG["starting_main_deck_size"]):
        """
        Loads star cards from JSON and builds a shuffled deck of total_cards.
        """
        with open(json_path, "r") as f:
            data = json.load(f)

        all_star_cards = [
            StarCard(
                name=item["name"],
                aura=item["aura"],
                talent=item["talent"],
                influence=item["influence"],
                legacy=item["legacy"],
                tags=item.get("tags", [])
            )
            for item in data
        ]

        selected_cards = random.sample(all_star_cards, k=min(total_cards, len(all_star_cards)))
        super().__init__(selected_cards)


class EventDeck(Deck):
    def __init__(self, json_path="resources/eventcards.json"):
        """
        Builds the event deck using the desired proportions:
        - 16 single-stat events
        - 12 choose-between-2 events
        - 2 ultimate showdowns (4-stat)
        """
        with open(json_path, "r") as f:
            all_events = json.load(f)

        # Split by type
        single_stat = [e for e in all_events if len(e["stat_options"]) == 1]
        double_stat = [e for e in all_events if len(e["stat_options"]) == 2]
        quad_stat = [e for e in all_events if len(e["stat_options"]) == 4]

        # Apply weighting
        event_defs = (
            single_stat * 4 +     # 4x each of 4 single-stat = 16
            double_stat * 2 +     # 2x each of 6 = 12
            quad_stat * 2         # 2x the 1 ultimate showdown = 2
        )

        # Build as StatContestEvent objects
        event_cards = [
            StatContestEvent(name=e["name"], stat_options=e["stat_options"])
            for e in event_defs
        ]

        # Shuffle and initialize the deck
        random.shuffle(event_cards)
        super().__init__(event_cards)
