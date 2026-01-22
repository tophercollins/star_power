"""
Simple AI for computer player that makes random decisions
"""
import random
import logging
from typing import Optional, Dict, Any
from engine.models.cards import StarCard, PowerCard, StealStarCard, EventCard

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

        # Try to play an event card (if we haven't already this turn and have stars)
        if game_engine.events_played_this_turn[self.player_index] < 1:
            if len(player.star_cards) > 0 and game_engine.current_event is None:
                if self._play_random_event(game_engine, player):
                    action_taken = True

        return action_taken

    def _play_random_star(self, game_engine, player) -> bool:
        """Try to play a random star card from hand"""
        from resources.config import GAME_CONFIG

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

        # Check if board is full and needs replacement
        max_stars = GAME_CONFIG["max_stars_on_board"]
        replace_star_index = None
        if len(player.star_cards) >= max_stars:
            # Board is full - pick the star with fewest fans to replace
            # This prevents losing valuable fans
            star_fan_counts = [(i, len(star.attached_fans)) for i, star in enumerate(player.star_cards)]

            # Sort by fan count (ascending) - stars with 0 fans first
            star_fan_counts.sort(key=lambda x: x[1])

            # Pick the star with the fewest fans (first in sorted list)
            replace_star_index = star_fan_counts[0][0]
            replaced_star = player.star_cards[replace_star_index]
            fan_count = len(replaced_star.attached_fans)

            logger.info(f"{player.name} (AI) replacing star: {replaced_star.name} ({fan_count} fans) with {card.name}")
        else:
            logger.info(f"{player.name} (AI) playing star: {card.name}")

        # Use the dispatch system to play the card
        command = {
            "type": "PLAY_CARD",
            "payload": {
                "player": self.player_index,
                "hand_index": hand_index,
                "replace_star_index": replace_star_index
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

        # Pick random power card
        hand_index = random.choice(power_indices)
        card = player.hand[hand_index]

        # Special handling for StealStarCard
        if isinstance(card, StealStarCard):
            return self._play_steal_card(game_engine, player, hand_index)

        # Regular power cards need own stars to target
        if not player.star_cards:
            logger.info(f"{player.name} has no stars to attach power cards to")
            return False

        # Pick random target star (own star)
        target_star_index = random.randint(0, len(player.star_cards) - 1)
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

    def _play_steal_card(self, game_engine, player, hand_index: int) -> bool:
        """Try to play a steal card - steal opponent's most valuable star"""
        from resources.config import GAME_CONFIG

        # Get opponent
        opponent_index = 1 - self.player_index
        opponent = game_engine.players[opponent_index]

        # Check if opponent has stars to steal
        if not opponent.star_cards:
            logger.info(f"{player.name} (AI) cannot steal - opponent has no stars")
            return False

        # Pick opponent's most valuable star (fans + power cards)
        opponent_star_values = []
        for i, star in enumerate(opponent.star_cards):
            fan_count = len(star.attached_fans)
            power_count = len(star.attached_power_cards)
            value = fan_count * 2 + power_count  # Fans worth more than powers
            opponent_star_values.append((i, value, star))

        # Sort by value (descending) - steal the most valuable star
        opponent_star_values.sort(key=lambda x: x[1], reverse=True)
        target_star_index, target_value, target_star = opponent_star_values[0]

        logger.info(f"{player.name} (AI) targeting opponent's {target_star.name} (value: {target_value})")

        # Check if AI's board is full and needs sacrifice
        max_stars = GAME_CONFIG["max_stars_on_board"]
        sacrifice_star_index = None

        if len(player.star_cards) >= max_stars:
            # Board is full - pick the star with fewest fans to sacrifice
            star_fan_counts = [(i, len(star.attached_fans)) for i, star in enumerate(player.star_cards)]
            star_fan_counts.sort(key=lambda x: x[1])
            sacrifice_star_index = star_fan_counts[0][0]
            sacrificed_star = player.star_cards[sacrifice_star_index]
            sacrificed_fan_count = len(sacrificed_star.attached_fans)
            logger.info(f"{player.name} (AI) will sacrifice {sacrificed_star.name} ({sacrificed_fan_count} fans)")

        card = player.hand[hand_index]
        logger.info(f"{player.name} (AI) playing '{card.name}' to steal {target_star.name}")

        # Use the dispatch system to play the steal card
        command = {
            "type": "PLAY_CARD",
            "payload": {
                "player": self.player_index,
                "hand_index": hand_index,
                "target_star_index": target_star_index,  # Opponent's star to steal
                "replace_star_index": sacrifice_star_index  # Own star to sacrifice if needed
            }
        }
        game_engine.dispatch(command)
        return True

    def _play_random_event(self, game_engine, player) -> bool:
        """Try to play a random event card with a random non-exhausted star"""
        event_indices = [
            i for i, card in enumerate(player.hand)
            if isinstance(card, EventCard)
        ]

        if not event_indices:
            logger.info(f"{player.name} has no event cards to play")
            return False

        # Pick random event card
        hand_index = random.choice(event_indices)
        card = player.hand[hand_index]

        # Find non-exhausted stars to compete with
        available_stars = [
            (i, star) for i, star in enumerate(player.star_cards)
            if not star.exhausted
        ]

        if not available_stars:
            logger.info(f"{player.name} (AI) has no non-exhausted stars to compete in event")
            return False

        # Pick random non-exhausted star
        target_star_index, target_star = random.choice(available_stars)

        logger.info(f"{player.name} (AI) playing event '{card.name}' with star '{target_star.name}'")

        # Use the dispatch system to play the event card
        command = {
            "type": "PLAY_CARD",
            "payload": {
                "player": self.player_index,
                "hand_index": hand_index,
                "target_star_index": target_star_index  # Star to compete in event
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
        from engine.models.cards import DoubleStatEvent

        # For double-stat events, return both stats (doesn't matter which order, system auto-selects)
        if isinstance(event, DoubleStatEvent):
            return f"{event.stat1}+{event.stat2}"  # Return string representation for logging

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
