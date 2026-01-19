import logging
from engine.models.cards import StarCard, PowerCard
from engine.rules.star_ops import play_star_from_hand
from engine.rules.power_ops import play_power_from_hand

logger = logging.getLogger(__name__)

def play_card_from_hand(player, hand_index: int, target_star_index: int = None):
    """
    Play a card from player's hand.

    Args:
        player: The player object
        hand_index: Index of card in hand
        target_star_index: Index of star to target (for power cards)

    Returns:
        None (mutates player state)
    """
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
        return play_power_from_hand(player, hand_index, target_star_index=target_star_index)

    else:
        logger.info(f"Unknown or unsupported card type: {type(card).__name__}")
        return