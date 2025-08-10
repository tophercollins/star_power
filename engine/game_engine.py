from typing import List, Dict, Any, Tuple
from engine.serializers import player_view, deck_view

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
        return self.snapshot()

    def snapshot(self) -> Dict[str, Any]:
        return {
            "turn": self.turn,
            "players": [player_view(player) for player in self.players],
            "main_deck": deck_view(self.main_deck),
            "event_deck": deck_view(self.event_deck),
            "fan_deck": deck_view(self.fan_deck),
            "log": list(self.log),
        }
    
    