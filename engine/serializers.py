from typing import List, Dict, Any

def player_view(player: Any) -> Dict[str, Any]:
        hand = getattr(player, "hand", [])
        played_stars = getattr(player, "played_stars", [])

        return {
            "name": getattr(player, "name", "Player"),
            "hand": [card_view(card) for card in hand],
            "played_stars": [card_view(star) for star in played_stars],
        }
    
def deck_view(deck: Any) -> Dict[str, Any]:
    return {
        "name": getattr(deck, "name", "Deck"),
        "size": len(deck.cards) if hasattr(deck, "cards") else 0,
    }

def card_view(card: Any) -> Dict[str, Any]:
    return {
        "name": getattr(card, "name", "Star"),
        "aura": getattr(card, "aura", 0),
        "influence": getattr(card, "influence", 0),
        "legacy": getattr(card, "legacy", 0),
        "talent": getattr(card, "talent", 0),
        "show_button": True,
        "button_label": "Play",
        "button_command": "Play",
        }
