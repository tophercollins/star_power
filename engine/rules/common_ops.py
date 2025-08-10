import logging
from engine.models.cards import StarCard, PowerCard
from engine.rules.star_ops import play_star_from_hand

logger = logging.getLogger(__name__)

def play_card_from_hand(player, hand_index: int, **kwargs):
    if hand_index is None:
        logger.info("Missing hand_index")
        return

    if hand_index < 0 or hand_index >= len(player.hand):
        logger.info("Invalid hand index")
        return

    card = player.hand[hand_index]

    if isinstance(card, StarCard):
        return play_star_from_hand(player, hand_index)

    elif isinstance(card, PowerCard):
        # Placeholder: wire this when power cards are ready
        logger.info(f"Playing PowerCard not implemented yet: {getattr(card, 'name', 'Unknown')}")
        return
        # Example for later:
        # target_star_index = kwargs.get("target_star_index")
        # return play_power_from_hand(player, hand_index, target_star_index=target_star_index)

    else:
        logger.info(f"Unknown or unsupported card type: {type(card).__name__}")
        return