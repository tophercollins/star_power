
GAME_CONFIG = {
    "starting_hand_size": 4,
    "cards_drawn_per_turn": 1,
    "star_cards_per_turn_limit": 1,
    "power_cards_per_turn_limit": 1,  # Reduced from 2 to 1
    "event_cards_per_turn_limit": 1,  # NEW - can play 1 event per turn
    "fans_to_win": 5,
    "max_stars_on_board": 3,  # Maximum stars each player can have on board
    "max_hand_size": 7,  # Maximum cards in hand
    "main_deck_composition": {
        "star_cards": 20,  # Total number of StarCards to include in the main deck
        "power_cards": 2,  # Number of each power card type to include in the main deck
        "event_cards": 1   # NEW - Number of each event card to include in the main deck
    },

    "fan_deck_composition": {
        "tag_superfans": 1,             # Number of tag-based SuperFan cards to include PER tag (e.g. 1 'Pop Superfan', 1 'Rapper Superfan', etc.)
        "tag_fans": 2,                  # Number of regular tag-based Fan cards to include PER tag (e.g. 2 'Pop Fans', 2 'DJ Fans', etc.)
        "generic_superfans": 2,         # Number of generic (non-tagged) SuperFan card to include
        "generic_fans": 10              # Number of generic (non-tagged) Fan card to include
    }
}

GOOGLE_SPREADSHEET_ID = "1CuN3CzMUi3YkNAEWqDReA2UoiKqvNBYu5WA_HzlAOHQ"