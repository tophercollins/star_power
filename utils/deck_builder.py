import random
import logging
from engine.models.deck import Deck
from engine.rules.deck_ops import shuffle_deck

from utils.card_loader import load_star_cards, load_power_cards, load_event_cards, load_fan_cards
from utils.google_client import google_sheets_client
from resources.config import GOOGLE_SPREADSHEET_ID, GAME_CONFIG

logger = logging.getLogger(__name__)

def build_main_deck_from_sheet(star_sheet, power_sheet):
    star_cards = load_star_cards(star_sheet)
    power_cards = load_power_cards(power_sheet)
    total_star_cards = GAME_CONFIG["main_deck_composition"]["star_cards"]
    total_power_cards = GAME_CONFIG["main_deck_composition"]["power_cards"]
    picked_star_cards = random.sample(star_cards, k=min(total_star_cards, len(star_cards)))
    picked_power_cards = []
    for card in power_cards:
        picked_power_cards.extend([card] * total_power_cards)
    picked_cards = picked_star_cards + picked_power_cards
    deck = Deck(name="Main Deck", cards=picked_cards)
    shuffle_deck(deck)
    return deck

def build_event_deck_from_sheet(sheet):
    event_cards = load_event_cards(sheet)

    single_stat = [event for event in event_cards if len(event.stat_options) == 1]
    double_stat = [event for event in event_cards if len(event.stat_options) == 2]
    quad_stat = [event for event in event_cards if len(event.stat_options) == 4]

    event_config = GAME_CONFIG["event_deck_composition"]

    combined_cards = (
        single_stat * event_config["single_stat_contest"]
        + double_stat * event_config["double_stat_contest"]
        + quad_stat * event_config["quad_stat_contest"]
    )

    random.shuffle(combined_cards)
    deck = Deck(name="Event Deck", cards=combined_cards)
    shuffle_deck(deck)
    return deck

def build_fan_deck_from_sheet(sheet):
    fan_cards = load_fan_cards(sheet)
    fan_config = GAME_CONFIG["fan_deck_composition"]

    tag_fans = [fan for fan in fan_cards if fan.bonus == 1 and fan.tag]
    tag_superfans = [fan for fan in fan_cards if fan.bonus == 2 and fan.tag]
    generic_fans = [fan for fan in fan_cards if fan.bonus == 1 and not fan.tag]
    generic_superfans = [fan for fan in fan_cards if fan.bonus == 2 and not fan.tag]

    deck_cards = []
    for fan in tag_fans:
        deck_cards.extend([fan] * fan_config["tag_fans"])
    for superfan in tag_superfans:
        deck_cards.extend([superfan] * fan_config["tag_superfans"])
    for fan in generic_fans:
        deck_cards.extend([fan] * fan_config["generic_fans"])
    for superfan in generic_superfans:
        deck_cards.extend([superfan] * fan_config["generic_superfans"])

    random.shuffle(deck_cards)
    deck = Deck(name="Fan Deck", cards=deck_cards)
    shuffle_deck(deck)
    return deck

def build_decks():
    logger.info("Accessing Google Sheets client")
    client = google_sheets_client()
    spreadsheet = client.open_by_key(GOOGLE_SPREADSHEET_ID)
    star_sheet = spreadsheet.worksheet("Star Cards")
    power_sheet = spreadsheet.worksheet("Power Cards")
    event_sheet = spreadsheet.worksheet("Event Cards")
    fan_sheet = spreadsheet.worksheet("Fan Cards")

    logger.info("Loading main, event, and fan decks from Google Sheets")
    main_deck = build_main_deck_from_sheet(star_sheet, power_sheet)
    logger.info("Main deck built with %d cards", len(main_deck.cards))
    event_deck = build_event_deck_from_sheet(event_sheet)
    logger.info("Event deck built with %d cards", len(event_deck.cards))
    fan_deck = build_fan_deck_from_sheet(fan_sheet)
    logger.info("Fan deck built with %d cards", len(fan_deck.cards))

    return main_deck, event_deck, fan_deck
