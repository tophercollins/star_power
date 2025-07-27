import logging
from classes.game_classes import Game

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    logging.info("Starting Star Power Game")
    game = Game()
    game.run()