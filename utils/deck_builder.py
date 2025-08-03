import random
import logging
from classes.deck_classes import Deck
from utils.card_loader import load_star_cards, load_event_cards, load_fan_cards
from utils.google_client import google_sheets_client
from resources.config import GOOGLE_SPREADSHEET_ID, GAME_CONFIG

logger = logging.getLogger(__name__)

def build_main_deck_from_sheet(sheet):
    star_cards = load_star_cards(sheet)
    total_star_cards = GAME_CONFIG["main_deck_composition"]["star_cards"]
    main_deck = random.sample(star_cards, k=min(total_star_cards, len(star_cards)))
    return Deck(main_deck)

def build_event_deck_from_sheet(sheet):
    event_cards = load_event_cards(sheet)

    single_stat = [e for e in event_cards if len(e.stat_options) == 1]
    double_stat = [e for e in event_cards if len(e.stat_options) == 2]
    quad_stat = [e for e in event_cards if len(e.stat_options) == 4]

    event_cfg = GAME_CONFIG["event_deck_composition"]

    event_deck = (
        single_stat * event_cfg["single_stat_contest"] +
        double_stat * event_cfg["double_stat_contest"] +
        quad_stat * event_cfg["quad_stat_contest"]
    )

    random.shuffle(event_deck)
    return Deck(event_deck)

def build_fan_deck_from_sheet(sheet):
    fan_cards = load_fan_cards(sheet)
    fan_config = GAME_CONFIG["fan_deck_composition"]

    tag_fans = [f for f in fan_cards if f.bonus == 1 and f.tag]
    tag_superfans = [f for f in fan_cards if f.bonus == 2 and f.tag]
    generic_fans = [f for f in fan_cards if f.bonus == 1 and not f.tag]
    generic_superfans = [f for f in fan_cards if f.bonus == 2 and not f.tag]

    # Create fan deck
    fan_deck = []

    # Add tag-based regular fans
    for fan in tag_fans:
        fan_deck.extend([fan] * fan_config["tag_fans"])  # e.g. 2 copies of each tag fan card

    # Add tag-based superfans
    for sf in tag_superfans:
        fan_deck.extend([sf] * fan_config["tag_superfans"])  # e.g. 1 copy of each tag superfan card

    # Add generic fans
    for fan in generic_fans:
        fan_deck.extend([fan] * fan_config["generic_fans"])  # e.g. 10 copies of each generic fan

    # Add generic superfans
    for sf in generic_superfans:
        fan_deck.extend([sf] * fan_config["generic_superfans"])  # e.g. 2 copies of each generic superfan

    random.shuffle(fan_deck)
    return Deck(fan_deck)

def build_decks():
    logger.info("Accessing Google Sheets client")
    client = google_sheets_client()
    spreadsheet_id = GOOGLE_SPREADSHEET_ID
    spreadsheet = client.open_by_key(spreadsheet_id)
    star_sheet = spreadsheet.worksheet("Star Cards")
    event_sheet = spreadsheet.worksheet("Event Cards")
    fan_sheet = spreadsheet.worksheet("Fan Cards")

    logger.info("Loading main, event, and fan decks from Google sheets")
    main_deck = build_main_deck_from_sheet(star_sheet)
    logger.info("Main deck built with %d cards", len(main_deck.cards))
    event_deck = build_event_deck_from_sheet(event_sheet)
    logger.info("Event deck built with %d cards", len(event_deck.cards))
    fan_deck = build_fan_deck_from_sheet(fan_sheet)
    logger.info("Fan deck built with %d cards", len(fan_deck.cards))

    return main_deck, event_deck, fan_deck
