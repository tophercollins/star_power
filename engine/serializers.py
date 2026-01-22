from typing import Any, Dict
from engine.models.cards import StarCard, PowerCard, ModifyStatCard, EventCard, StatContestEvent, DoubleStatEvent

def star_card_view(card) -> dict:
    return {
        "id": getattr(card, "id", None),
        "type": "StarCard",
        "name": getattr(card, "name", "Star"),
        "aura": getattr(card, "aura", 0),
        "influence": getattr(card, "influence", 0),
        "talent": getattr(card, "talent", 0),
        "legacy": getattr(card, "legacy", 0),
        "exhausted": getattr(card, "exhausted", False),
        "attached_power_cards": [
            power_card_view(p) for p in getattr(card, "attached_power_cards", [])
        ],
        "attached_fans": [
            {"id": f.id, "name": f.name, "bonus": f.bonus, "tag": f.tag}
            for f in getattr(card, "attached_fans", [])
        ],
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

        elif isinstance(c, EventCard):
            v = event_view(c)
            # Human can play events if they have stars on board (need a star to compete with)
            if player_index == 0 and has_star_cards:
                v["show_button"] = True
                v["button_label"] = "Play Event"
                v["button_command"] = {
                    "type": "PLAY_CARD",
                    "payload": {"player": player_index, "hand_index": i}
                }
            else:
                v["show_button"] = False

        else:
            # Fallback for unknown types
            v = {"id": getattr(c, "id", None), "type": c.__class__.__name__, "name": getattr(c, "name", "Card"), "show_button": False}

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

def event_view(event: Any) -> Dict[str, Any]:
    """Serialize event card for UI display"""
    if event is None:
        return None

    base = {
        "id": getattr(event, "id", None),
        "name": getattr(event, "name", "Event"),
        "description": getattr(event, "description", ""),
        "event_type": getattr(event, "event_type", "basic"),
        "fan_reward": getattr(event, "fan_reward", 1),
    }

    # Add type-specific fields
    if hasattr(event, "stat_options"):
        base["stat_options"] = event.stat_options
    if hasattr(event, "contest_type"):
        base["contest_type"] = event.contest_type
    if hasattr(event, "required_stats"):
        base["required_stats"] = event.required_stats
    if hasattr(event, "required_stat"):
        base["required_stat"] = event.required_stat
        base["threshold"] = getattr(event, "threshold", 0)
    if hasattr(event, "required_tags"):
        base["required_tags"] = event.required_tags
    if hasattr(event, "winning_stat"):
        base["winning_stat"] = event.winning_stat
    if hasattr(event, "fan_penalty"):
        base["fan_penalty"] = event.fan_penalty

    # Double-stat event fields
    if hasattr(event, "stat1"):
        base["stat1"] = event.stat1
    if hasattr(event, "stat2"):
        base["stat2"] = event.stat2

    return base
