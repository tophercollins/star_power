import random
import logging
from engine.models.deck import Deck
from engine.rules.deck_ops import shuffle_deck
from resources.config import GAME_CONFIG

# Import hardcoded card data instead of Google Sheets
from resources.card_data import get_star_cards, get_power_cards, get_event_cards, get_fan_cards

logger = logging.getLogger(__name__)

def build_main_deck_from_cards():
    """Build main deck from hardcoded card data - includes stars, powers, AND events"""
    star_cards = get_star_cards()
    power_cards = get_power_cards()
    event_cards = get_event_cards()

    total_star_cards = GAME_CONFIG["main_deck_composition"]["star_cards"]
    total_power_cards = GAME_CONFIG["main_deck_composition"]["power_cards"]
    total_event_cards = GAME_CONFIG["main_deck_composition"]["event_cards"]

    # Sample stars
    picked_star_cards = random.sample(star_cards, k=min(total_star_cards, len(star_cards)))

    # Duplicate power cards
    picked_power_cards = []
    for card in power_cards:
        picked_power_cards.extend([card] * total_power_cards)

    # Duplicate event cards - NEW: events are now in main deck
    picked_event_cards = []
    for card in event_cards:
        picked_event_cards.extend([card] * total_event_cards)

    # Combine and shuffle - stars + powers + events
    picked_cards = picked_star_cards + picked_power_cards + picked_event_cards
    deck = Deck(name="Main Deck", cards=picked_cards)
    shuffle_deck(deck)
    logger.info(f"Main deck built: {len(picked_star_cards)} stars, {len(picked_power_cards)} powers, {len(picked_event_cards)} events")
    return deck

def build_event_deck_from_cards():
    """Build event deck from hardcoded card data"""
    event_cards = get_event_cards()

    # Use all event cards - the new system has 23 diverse events
    # No need to categorize by stat_options since we have varied event types
    deck = Deck(name="Event Deck", cards=event_cards)
    shuffle_deck(deck)
    logger.info(f"Event deck built with {len(event_cards)} cards across 6 event types")
    return deck

def build_fan_deck_from_cards():
    """Build fan deck from hardcoded card data"""
    fan_cards = get_fan_cards()

    deck = Deck(name="Fan Deck", cards=fan_cards)
    shuffle_deck(deck)
    return deck

def build_decks():
    """Build all three decks from hardcoded card data"""
    logger.info("Building decks from hardcoded card data")

    main_deck = build_main_deck_from_cards()
    logger.info("Main deck built with %d cards", len(main_deck.cards))

    event_deck = build_event_deck_from_cards()
    logger.info("Event deck built with %d cards", len(event_deck.cards))

    fan_deck = build_fan_deck_from_cards()
    logger.info("Fan deck built with %d cards", len(fan_deck.cards))

    return main_deck, event_deck, fan_deck
