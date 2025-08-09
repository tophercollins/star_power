from typing import List, Dict, Any, Tuple

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
            "players": [self._player_view(player) for player in self.players],
            "main_deck": self._deck_view(self.main_deck),
            "event_deck": self._deck_view(self.event_deck),
            "fan_deck": self._deck_view(self.fan_deck),
            "log": list(self.log),
        }
    
    def _player_view(self, player: Any) -> Dict[str, Any]:
        hand = getattr(player, "hand", [])
        return {
            "name": getattr(player, "name", "Player"),
            "hand": [self._card_view(card) for card in hand]
        }
    
    def _deck_view(self, deck: Any) -> Dict[str, Any]:
        return {
            "name": getattr(deck, "name", "Deck"),
            "size": len(deck.cards) if hasattr(deck, "cards") else 0,
        }

    def _card_view(self, card: Any) -> Dict[str, Any]:
        return {
            "name": getattr(card, "name", "Star"),
            "aura": getattr(card, "aura", 0),
            "influence": getattr(card, "influence", 0),
            "legacy": getattr(card, "legacy", 0),
            "talent": getattr(card, "talent", 0),
        }
