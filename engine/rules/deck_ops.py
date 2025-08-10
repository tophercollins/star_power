import random
from typing import List, Any
from engine.models.deck import Deck
import logging

logger = logging.getLogger(__name__)

def shuffle_deck(deck: Deck) -> None:
    random.shuffle(deck.cards)

def draw_card(deck: Deck) -> Any | None:
    logger.info(f"Drawing card from {deck.name} with {len(deck.cards)} cards")
    if not deck.cards:
        return None
    return deck.cards.pop(0)

def add_card(deck: Deck, card: Any) -> None:
    deck.cards.append(card)

def add_many_cards(deck: Deck, cards: List[Any]) -> None:
    deck.cards.extend(cards)

def peek_cards(deck: Deck, count: int = 1) -> List[Any]:
    return deck.cards[:count]

def deck_size(deck: Deck) -> int:
    return len(deck.cards)

def is_deck_empty(deck: Deck) -> bool:
    return len(deck.cards) == 0
