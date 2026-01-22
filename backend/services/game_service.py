"""
Game Service - Business logic layer
Wraps the game engine and manages game state
"""
import sys
import os
import uuid
import logging
from typing import Dict, Any, Optional, Tuple, List

# Add parent directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from engine.game_engine import GameEngine
from engine.setup import build_players, build_decks, deal_starting_hands

logger = logging.getLogger(__name__)

class GameService:
    """
    Service layer for game management.

    Currently stores games in memory. Will be replaced with database persistence
    in future versions.
    """

    def __init__(self):
        """Initialize the game service with in-memory storage"""
        self.active_games: Dict[str, GameEngine] = {}
        logger.info("GameService initialized (in-memory mode)")

    def create_game(self, player1_name: str, player2_name: str = "Computer") -> Tuple[str, Dict[str, Any]]:
        """
        Create a new game.

        Args:
            player1_name: Name for player 1
            player2_name: Name for player 2 (defaults to "Computer")

        Returns:
            Tuple of (game_id, initial_game_state)
        """
        try:
            # Generate unique game ID
            game_id = str(uuid.uuid4())

            logger.info(f"Creating game {game_id}: {player1_name} vs {player2_name}")

            # Build players
            players = build_players()
            players[0].name = player1_name
            players[0].is_human = True
            players[1].name = player2_name
            players[1].is_human = (player2_name != "Computer")

            # Build decks
            logger.info(f"Building decks for game {game_id}")
            main_deck, event_deck, fan_deck = build_decks()

            # Deal starting hands
            logger.info(f"Dealing starting hands for game {game_id}")
            deal_starting_hands(players, main_deck)

            # Create game engine
            engine = GameEngine(
                players=players,
                decks=(main_deck, event_deck, fan_deck)
            )

            # Store in memory
            self.active_games[game_id] = engine

            # Get initial state
            state = engine.snapshot()

            logger.info(f"Game {game_id} created successfully")
            logger.info(f"Player 1: {players[0].name} - {len(players[0].hand)} cards in hand")
            logger.info(f"Player 2: {players[1].name} - {len(players[1].hand)} cards in hand")

            return game_id, state

        except Exception as e:
            logger.error(f"Failed to create game: {str(e)}", exc_info=True)
            raise

    def get_game_state(self, game_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the current state of a game.

        Args:
            game_id: Unique game identifier

        Returns:
            Game state dictionary or None if game not found
        """
        if game_id not in self.active_games:
            logger.warning(f"Game not found: {game_id}")
            return None

        engine = self.active_games[game_id]
        return engine.snapshot()

    def play_card(self, game_id: str, player_index: int, hand_index: int, target_star_index: int = None, replace_star_index: int = None) -> Optional[Dict[str, Any]]:
        """
        Play a card from a player's hand.

        Args:
            game_id: Unique game identifier
            player_index: Which player (0 or 1)
            hand_index: Position of card in hand
            target_star_index: Index of star to target (for power cards)
            replace_star_index: Index of star on board to replace (when board is full)

        Returns:
            Updated game state or None if game not found
        """
        if game_id not in self.active_games:
            logger.warning(f"Game not found: {game_id}")
            return None

        engine = self.active_games[game_id]

        # Build command for game engine
        command = {
            "type": "PLAY_CARD",
            "payload": {
                "player": player_index,
                "hand_index": hand_index,
                "target_star_index": target_star_index,
                "replace_star_index": replace_star_index
            }
        }

        logger.info(f"Game {game_id}: Player {player_index} playing card at index {hand_index}, target={target_star_index}, replace={replace_star_index}")

        # Dispatch to engine
        try:
            # The engine dispatch calls the rule functions and returns updated state
            result = engine.dispatch(command)
            logger.info(f"Game {game_id}: Card played successfully")
            return result
        except Exception as e:
            logger.error(f"Error playing card in game {game_id}: {str(e)}", exc_info=True)
            raise

    def delete_game(self, game_id: str) -> bool:
        """
        Delete a game.

        Args:
            game_id: Unique game identifier

        Returns:
            True if game was deleted, False if not found
        """
        if game_id in self.active_games:
            del self.active_games[game_id]
            logger.info(f"Game deleted: {game_id}")
            return True

        logger.warning(f"Cannot delete game (not found): {game_id}")
        return False

    def list_games(self) -> List[str]:
        """
        List all active game IDs.

        Returns:
            List of game IDs
        """
        return list(self.active_games.keys())

    def get_game_count(self) -> int:
        """
        Get the number of active games.

        Returns:
            Number of active games
        """
        return len(self.active_games)

    def end_turn(self, game_id: str) -> Optional[Dict[str, Any]]:
        """
        End the current turn and progress game state.

        Args:
            game_id: Unique game identifier

        Returns:
            Updated game state or None if game not found
        """
        if game_id not in self.active_games:
            logger.warning(f"Game not found: {game_id}")
            return None

        engine = self.active_games[game_id]

        # Build END_TURN command
        command = {
            "type": "END_TURN",
            "payload": {}
        }

        logger.info(f"Game {game_id}: Ending turn for player {engine.current_player_index} in round {engine.round}")

        # Dispatch to engine
        try:
            result = engine.dispatch(command)
            logger.info(f"Game {game_id}: Turn ended, now round {engine.round}, phase: {engine.phase}")
            return result
        except Exception as e:
            logger.error(f"Error ending turn in game {game_id}: {str(e)}", exc_info=True)
            raise

    def select_star_for_event(
        self,
        game_id: str,
        player_index: int,
        star_index: int,
        stat: str
    ) -> Optional[Dict[str, Any]]:
        """
        Select a star and stat for the current event.

        Args:
            game_id: Unique game identifier
            player_index: Which player (0 or 1)
            star_index: Index of star on player's board
            stat: Stat to use for contest

        Returns:
            Updated game state or None if game not found
        """
        if game_id not in self.active_games:
            logger.warning(f"Game not found: {game_id}")
            return None

        engine = self.active_games[game_id]

        # Build SELECT_STAR_FOR_EVENT command
        command = {
            "type": "SELECT_STAR_FOR_EVENT",
            "payload": {
                "player": player_index,
                "star_index": star_index,
                "stat": stat
            }
        }

        logger.info(f"Game {game_id}: Player {player_index} selecting star {star_index} with stat {stat}")

        # Dispatch to engine
        try:
            result = engine.dispatch(command)
            logger.info(f"Game {game_id}: Star selected, phase: {engine.phase}")
            return result
        except Exception as e:
            logger.error(f"Error selecting star in game {game_id}: {str(e)}", exc_info=True)
            raise

# TODO: Replace with database-backed service
# class DatabaseGameService(GameService):
#     """
#     Database-backed game service using Supabase/PostgreSQL
#     """
#     def __init__(self, database_url: str):
#         self.db = create_engine(database_url)
#         # Implement database persistence methods
