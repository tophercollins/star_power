from typing import Any, Dict

def star_card_view(card) -> dict:
    return {
        "name": getattr(card, "name", "Star"),
        "aura": getattr(card, "aura", 0),
        "influence": getattr(card, "influence", 0),
        "talent": getattr(card, "talent", 0),
        "legacy": getattr(card, "legacy", 0),
    }

def player_view(player: Any, player_index: int = 0) -> Dict[str, Any]:
    hand_views = []
    for i, c in enumerate(getattr(player, "hand", [])):
        # Base card data (works for all card types)
        v = {
            "name": getattr(c, "name", "Card"),
            "aura": getattr(c, "aura", 0),
            "influence": getattr(c, "influence", 0),
            "talent": getattr(c, "talent", 0),
            "legacy": getattr(c, "legacy", 0),
        }

        # For now: allow Play only for StarCards in human player's hand
        if c.__class__.__name__ == "StarCard" and player_index == 0:
            v["show_button"] = True
            v["button_label"] = "Play"
            v["button_command"] = {
                "type": "PLAY_CARD",
                "payload": {"player": player_index, "hand_index": i}
            }
        else:
            v["show_button"] = False

        hand_views.append(v)

    return {
        "name": getattr(player, "name", "Player"),
        "hand": hand_views,
        "stars": [star_card_view(c) for c in getattr(player, "star_cards", [])],
    }

def deck_view(deck: Any) -> Dict[str, Any]:
    return {
        "name": getattr(deck, "name", "Deck"),
        "size": len(deck.cards) if hasattr(deck, "cards") else 0,
    }
