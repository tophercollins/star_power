from typing import Any, Dict
from engine.models.cards import StarCard, PowerCard, ModifyStatCard

def star_card_view(card) -> dict:
    return {
        "id": getattr(card, "id", None),
        "type": "StarCard",
        "name": getattr(card, "name", "Star"),
        "aura": getattr(card, "aura", 0),
        "influence": getattr(card, "influence", 0),
        "talent": getattr(card, "talent", 0),
        "legacy": getattr(card, "legacy", 0),
    }

def power_card_view(card) -> dict:
    return {
        "id": getattr(card, "id", None),
        "type": "ModifyStatCard" if isinstance(card, ModifyStatCard) else "PowerCard",
        "name": getattr(card, "name", "Power"),
        "description": getattr(card, "description", ""),
        "targets_star": getattr(card, "targets_star", False),
        "stat_modifiers": getattr(card, "stat_modifiers", {}),
    }

def player_view(player: Any, player_index: int = 0) -> Dict[str, Any]:
    has_star_cards = bool(getattr(player, "star_cards", []))

    hand_views = []
    for i, c in enumerate(getattr(player, "hand", [])):
        # Build per-type payload
        if isinstance(c, StarCard):
            v = star_card_view(c)
            # Human can play stars from hand
            if player_index == 0:
                v["show_button"] = True
                v["button_label"] = "Play"
                v["button_command"] = {
                    "type": "PLAY_CARD",
                    "payload": {"player": player_index, "hand_index": i}
                }
            else:
                v["show_button"] = False

        elif isinstance(c, PowerCard):
            v = power_card_view(c)
            # Human can only play powers if they already have a star on board
            if player_index == 0 and has_star_cards and v.get("targets_star", False):
                v["show_button"] = True
                v["button_label"] = "Play"
                v["button_command"] = {
                    "type": "PLAY_CARD",
                    "payload": {"player": player_index, "hand_index": i}
                }
            else:
                v["show_button"] = False

        else:
            # Fallback for unknown types
            v = {"id": getattr(card, "id", None), "type": c.__class__.__name__, "name": getattr(c, "name", "Card"), "show_button": False}

        hand_views.append(v)

    return {
        "name": getattr(player, "name", "Player"),
        "hand": hand_views,
        "stars": [star_card_view(s) for s in getattr(player, "star_cards", [])],
    }

def deck_view(deck: Any) -> Dict[str, Any]:
    return {
        "name": getattr(deck, "name", "Deck"),
        "size": len(deck.cards) if hasattr(deck, "cards") else 0,
    }
