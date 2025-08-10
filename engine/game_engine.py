from typing import List, Dict, Any, Tuple
from engine.serializers import player_view, deck_view
from engine.rules.common_ops import play_card_from_hand

class GameEngine:
    def __init__(self, players: List[Any], decks: Tuple[Any, Any, Any]):
        self.players = players
        self.main_deck, self.event_deck, self.fan_deck = decks
        self.turn = 1
        self.log = ["Game started"]

    def dispatch(self, command: dict) -> Dict[str, Any]:
        action = command.get("type")
        payload = command.get("payload", {})
        self.log.append(f"Dispatch: {action} {payload}")

        if action == "PLAY_CARD":
            player = payload.get("player", 0)
            hand_index = payload.get("hand_index")
            if 0 <= player < len(self.players):
                play_card_from_hand(self.players[player], hand_index, self.log)
            else:
                self.log.append(f"Invalid player index: {player}")

        return self.snapshot()

    def snapshot(self) -> Dict[str, Any]:
        return {
            "turn": self.turn,
            "players": [player_view(player, player_index=i) for i, player in enumerate(self.players)],
            "main_deck": deck_view(self.main_deck),
            "event_deck": deck_view(self.event_deck),
            "fan_deck": deck_view(self.fan_deck),
            "log": list(self.log),
        }
    
    