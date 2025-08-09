import logging
from engine.game_engine import GameEngine
from engine.setup import build_players, build_decks, deal_starting_hands
from ui.game_client import GameClient

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logging.info("Starting Star Power Game")

    players = build_players()
    main_deck, event_deck, fan_deck = build_decks()
    deal_starting_hands(players, main_deck)

    engine = GameEngine(
        players=players,
        decks=(main_deck, event_deck, fan_deck)
    )

    GameClient(engine)
