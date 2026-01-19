from typing import List, Dict, Any, Tuple, Optional
from engine.serializers import player_view, deck_view
from engine.rules.common_ops import play_card_from_hand
# from engine.rules.power_ops import attach_power_by_ids
from engine.models.cards import StarCard, PowerCard
import logging

logger = logging.getLogger(__name__)

class GameEngine:
    def __init__(self, players: List[Any], decks: Tuple[Any, Any, Any]):
        logger.info("Initializing GameEngine")
        self.players = players
        self.main_deck, self.event_deck, self.fan_deck = decks
        self.turn = 1

        self.pending_card: Optional[Dict[str, Any]] = None

    def dispatch(self, command: dict) -> Dict[str, Any]:
        action = command.get("type")
        payload = command.get("payload", {})
        logger.info(f"Dispatch: {action} {payload}")

        if action == "PLAY_CARD":
            player_index = payload.get("player", 0)
            hand_index = payload.get("hand_index")

            if 0 <= player_index < len(self.players):
                player = self.players[player_index]

                # Validate hand_index and get the card
                if hand_index is None or hand_index < 0 or hand_index >= len(player.hand):
                    logger.warning(f"Invalid hand index {hand_index} for player {player.name}")
                    return self.snapshot()

                # Delegate to common_ops which handles all card types
                play_card_from_hand(player, hand_index)
            else:
                logger.warning(f"Invalid player index: {player_index}")

        return self.snapshot()

    def snapshot(self) -> Dict[str, Any]:
        return {
            "turn": self.turn,
            "players": [player_view(player, player_index=i) for i, player in enumerate(self.players)],
            "main_deck": deck_view(self.main_deck),
            "event_deck": deck_view(self.event_deck),
            "fan_deck": deck_view(self.fan_deck),
        }
    
    