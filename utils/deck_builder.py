import random
from classes.deck_classes import Deck
from card_loader import load_star_cards, load_event_cards, load_fan_cards
from utils.google_client import google_sheets_client
from resources.config import GOOGLE_SPREADSHEET_ID, GAME_CONFIG

def build_main_deck_from_sheet(sheet):
    all_cards = load_star_cards(sheet)
    total = GAME_CONFIG["starting_main_deck_size"]
    selected = random.sample(all_cards, k=min(total, len(all_cards)))
    return Deck(selected)

def build_event_deck_from_sheet(sheet):
    all_events = load_event_cards(sheet)

    single_stat = [e for e in all_events if len(e.stat_options) == 1]
    double_stat = [e for e in all_events if len(e.stat_options) == 2]
    quad_stat = [e for e in all_events if len(e.stat_options) == 4]

    event_defs = (
        single_stat * 4 +
        double_stat * 2 +
        quad_stat * 2
    )

    random.shuffle(event_defs)
    return Deck(event_defs)

def build_fan_deck_from_sheet(sheet):
    all_fans = load_fan_cards(sheet)

    tag_superfans = [f for f in all_fans if f.bonus == 2 and f.condition_tag]
    tag_fans = [f for f in all_fans if f.bonus == 1 and f.condition_tag]
    generic_superfans = [f for f in all_fans if f.bonus == 2 and not f.condition_tag]
    generic_fans = [f for f in all_fans if f.bonus == 1 and not f.condition_tag]

    deck_cards = []

    # 1 of each tag superfan (6 total)
    used_tags = set()
    for fan in tag_superfans:
        if fan.condition_tag not in used_tags:
            deck_cards.append(fan)
            used_tags.add(fan.condition_tag)
        if len(used_tags) == 6:
            break

    # 2 of each tag fan (12 total)
    tag_fan_counts = {}
    for fan in tag_fans:
        tag = fan.condition_tag
        if tag_fan_counts.get(tag, 0) < 2:
            deck_cards.append(fan)
            tag_fan_counts[tag] = tag_fan_counts.get(tag, 0) + 1
        if sum(tag_fan_counts.values()) == 12:
            break

    # 2 generic superfans
    deck_cards.extend(generic_superfans[:2])

    # 12 generic fans
    deck_cards.extend(generic_fans[:12])

    random.shuffle(deck_cards)
    return Deck(deck_cards)

def build_decks():
    client = google_sheets_client()
    spreadsheet_id = GOOGLE_SPREADSHEET_ID
    star_sheet = client.open_by_key(spreadsheet_id).worksheet("Star Cards")
    event_sheet = client.open_by_key(spreadsheet_id).worksheet("Event Cards")
    fan_sheet = client.open_by_key(spreadsheet_id).worksheet("Fan Cards")

    main_deck = build_main_deck_from_sheet(star_sheet)
    event_deck = build_event_deck_from_sheet(event_sheet)
    fan_deck = build_fan_deck_from_sheet(fan_sheet)

    return main_deck, event_deck, fan_deck
