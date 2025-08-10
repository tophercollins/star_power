
GAME_CONFIG = {
    "starting_hand_size": 4,
    "cards_drawn_per_turn": 1,
    "star_cards_per_turn_limit": 1,
    "power_cards_per_turn_limit": 2,
    "event_start_turn": 2,    
    "fans_to_win": 10,
    "main_deck_composition": {
        "star_cards": 20,  # Total number of StarCards to include in the main deck
        "power_cards": 2   # Number of each power card type to include in the main deck
    },

    "fan_deck_composition": {
        "tag_superfans": 1,             # Number of tag-based SuperFan cards to include PER tag (e.g. 1 'Pop Superfan', 1 'Rapper Superfan', etc.)
        "tag_fans": 2,                  # Number of regular tag-based Fan cards to include PER tag (e.g. 2 'Pop Fans', 2 'DJ Fans', etc.)
        "generic_superfans": 2,         # Number of generic (non-tagged) SuperFan card to include
        "generic_fans": 10              # Number of generic (non-tagged) Fan card to include
    },

    "event_deck_composition": {
        "single_stat_contest": 4,   # Number of EventCards that contest a single stat (e.g. "Rap Battle" for Talent)
        "double_stat_contest": 2,    # Number of EventCards that contest two stat options (player chooses one from two)
        "quad_stat_contest": 2      # Number of EventCards that involve all four stats (player chooses one from four)
    }
}

GOOGLE_SPREADSHEET_ID = "1CuN3CzMUi3YkNAEWqDReA2UoiKqvNBYu5WA_HzlAOHQ"