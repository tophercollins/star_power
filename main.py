import logging
from classes.game_classes import Game
from ui.game_client import GameClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    logging.info("Starting Star Power Game")
    game = Game()
    GameClient(game)
