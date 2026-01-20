"""
Simple AI for computer player that makes random decisions
"""
import random
import logging
from typing import Optional, Dict, Any
from engine.models.cards import StarCard, PowerCard

logger = logging.getLogger(__name__)


class ComputerPlayer:
    """Basic AI that makes random card plays and event selections"""

    def __init__(self, player_index: int = 1):
        self.player_index = player_index

    def take_turn(self, game_engine) -> bool:
        """
        Execute computer's turn - play cards randomly
        Returns True if any action was taken
        """
        player = game_engine.players[self.player_index]
        action_taken = False

        # Try to play a star card (if we haven't already this turn)
        if game_engine.stars_played_this_turn[self.player_index] < 1:
            if self._play_random_star(game_engine, player):
                action_taken = True

        # Try to play a power card (if we haven't already this turn and have stars)
        if game_engine.powers_played_this_turn[self.player_index] < 1:
            if len(player.star_cards) > 0:
                if self._play_random_power(game_engine, player):
                    action_taken = True

        return action_taken

    def _play_random_star(self, game_engine, player) -> bool:
        """Try to play a random star card from hand"""
        star_indices = [
            i for i, card in enumerate(player.hand)
            if isinstance(card, StarCard)
        ]

        if not star_indices:
            logger.info(f"{player.name} has no star cards to play")
            return False

        # Pick random star card
        hand_index = random.choice(star_indices)
        card = player.hand[hand_index]

        logger.info(f"{player.name} (AI) playing star: {card.name}")

        # Use the dispatch system to play the card
        command = {
            "type": "PLAY_CARD",
            "payload": {
                "player": self.player_index,
                "hand_index": hand_index
            }
        }
        game_engine.dispatch(command)
        return True

    def _play_random_power(self, game_engine, player) -> bool:
        """Try to play a random power card on a random star"""
        power_indices = [
            i for i, card in enumerate(player.hand)
            if isinstance(card, PowerCard)
        ]

        if not power_indices:
            logger.info(f"{player.name} has no power cards to play")
            return False

        if not player.star_cards:
            logger.info(f"{player.name} has no stars to attach power cards to")
            return False

        # Pick random power card and random target star
        hand_index = random.choice(power_indices)
        target_star_index = random.randint(0, len(player.star_cards) - 1)

        card = player.hand[hand_index]
        target = player.star_cards[target_star_index]

        logger.info(f"{player.name} (AI) playing power '{card.name}' on '{target.name}'")

        # Use the dispatch system to play the card
        command = {
            "type": "PLAY_CARD",
            "payload": {
                "player": self.player_index,
                "hand_index": hand_index,
                "target_star_index": target_star_index
            }
        }
        game_engine.dispatch(command)
        return True

    def select_for_event(self, game_engine, event) -> Optional[Dict[str, Any]]:
        """
        Select a star and stat for an event
        Returns {"star_index": int, "stat": str} or None
        """
        player = game_engine.players[self.player_index]

        if not player.star_cards:
            logger.info(f"{player.name} has no stars to compete in event")
            return None

        # Filter out exhausted stars
        available_stars = [
            (i, star) for i, star in enumerate(player.star_cards)
            if not star.exhausted
        ]

        if not available_stars:
            logger.info(f"{player.name} has no non-exhausted stars available")
            return None

        # Pick random non-exhausted star
        star_index, star = random.choice(available_stars)

        # Determine available stats for this event
        stat = self._choose_stat_for_event(event, star)

        if stat:
            logger.info(f"{player.name} (AI) selecting '{star.name}' with stat '{stat}' for event")
            return {"star_index": star_index, "stat": stat}

        return None

    def _choose_stat_for_event(self, event, star) -> Optional[str]:
        """Choose which stat to use for this event"""
        # For events with stat_options, pick randomly
        if hasattr(event, 'stat_options') and event.stat_options:
            return random.choice(event.stat_options)

        # For events with winning_stat (tag/threshold events), use that
        if hasattr(event, 'winning_stat'):
            return event.winning_stat

        # For combined stat events, pick any stat (doesn't matter)
        if hasattr(event, 'required_stats'):
            return "aura"  # Default, doesn't affect combined calculation

        # Default fallback
        return random.choice(["aura", "talent", "influence", "legacy"])
