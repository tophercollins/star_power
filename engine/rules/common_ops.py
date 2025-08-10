from engine.models.cards import StarCard, PowerCard
from engine.rules.star_ops import play_star_from_hand
# from engine.rules.power_ops import play_power_from_hand

def play_card_from_hand(player, hand_index: int, log: list, **kwargs):
    if hand_index is None:
        log.append("Missing hand_index")
        return

    if hand_index < 0 or hand_index >= len(player.hand):
        log.append("Invalid hand index")
        return

    card = player.hand[hand_index]

    if isinstance(card, StarCard):
        return play_star_from_hand(player, hand_index, log)

    elif isinstance(card, PowerCard):
        # Placeholder: wire this when power cards are ready
        log.append(f"Playing PowerCard not implemented yet: {getattr(card, 'name', 'Unknown')}")
        return
        # Example for later:
        # target_star_index = kwargs.get("target_star_index")
        # return play_power_from_hand(player, hand_index, log, target_star_index=target_star_index)

    else:
        log.append(f"Unknown or unsupported card type: {type(card).__name__}")
        return