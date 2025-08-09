from typing import List, Tuple
from resources.config import GAME_CONFIG
from engine.models.player import Player
from engine.models.deck import Deck
from engine.rules.deck_ops import draw_card
from utils.deck_builder import build_decks as deck_builder


def build_players() -> List[Player]:
    """
    Create the player list (data only).
    """
    return [
        Player(name="Toph", is_human=True),
        Player(name="Computer", is_human=False),
    ]


def build_decks() -> Tuple[Deck, Deck, Deck]:
    """
    Build the three decks from the deck builder and wrap them
    in our model Deck class.
    """
    main, event, fan = deck_builder()

    main_deck = Deck(name=getattr(main, "name", "Main Deck"),
                     cards=list(getattr(main, "cards", [])))
    event_deck = Deck(name=getattr(event, "name", "Event Deck"),
                      cards=list(getattr(event, "cards", [])))
    fan_deck = Deck(name=getattr(fan, "name", "Fan Deck"),
                    cards=list(getattr(fan, "cards", [])))

    return main_deck, event_deck, fan_deck

def deal_starting_hands(players: List[Player], main_deck: Deck) -> None:
    """
    Deal starting hands to players.
    """
    hand_size = GAME_CONFIG["starting_hand_size"]
    for player in players:
        for _ in range(hand_size):
            card = draw_card(main_deck)
            if card:
                player.hand.append(card)

def engine_config() -> dict:
    """
    Extract engine-level config values (no behavior).
    """
    return {
        "turn": 1,
        "event_start_turn": GAME_CONFIG["event_start_turn"],
        "fans_to_win": GAME_CONFIG["fans_to_win"],
        "starting_hand_size": GAME_CONFIG["starting_hand_size"],
        "cards_drawn_per_turn": GAME_CONFIG["cards_drawn_per_turn"],
        "star_cards_per_turn_limit": GAME_CONFIG["star_cards_per_turn_limit"],
        "power_cards_per_turn_limit": GAME_CONFIG["power_cards_per_turn_limit"],
    }
