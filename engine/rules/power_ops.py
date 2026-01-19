"""
Power Card Operations - Playing power cards and applying stat modifications
"""
import logging
from engine.models.cards import PowerCard, ModifyStatCard, StarCard

logger = logging.getLogger(__name__)


def play_power_from_hand(player, hand_index: int, target_star_index: int = None):
    """
    Play a power card from player's hand onto one of their stars.

    Args:
        player: The player object
        hand_index: Index of power card in hand
        target_star_index: Index of star on player's board to attach to

    Returns:
        None (mutates player state)
    """
    # Validate hand index
    if hand_index is None or hand_index < 0 or hand_index >= len(player.hand):
        logger.warning(f"Invalid hand index: {hand_index}")
        return

    card = player.hand[hand_index]

    # Validate it's a power card
    if not isinstance(card, PowerCard):
        logger.warning(f"Card at index {hand_index} is not a PowerCard: {type(card).__name__}")
        return

    # Check if player has any stars to target
    if len(player.star_cards) == 0:
        logger.warning(f"{player.name} has no stars to attach power card to")
        return

    # Validate target star index
    if target_star_index is None or target_star_index < 0 or target_star_index >= len(player.star_cards):
        logger.warning(f"Invalid target star index: {target_star_index}")
        return

    target_star = player.star_cards[target_star_index]

    # Apply card effects based on type
    if isinstance(card, ModifyStatCard):
        _apply_stat_modifiers(target_star, card)

    # Attach power card to star
    target_star.attached_power_cards.append(card)

    # Remove from hand
    player.hand.pop(hand_index)

    logger.info(f"{player.name} played '{card.name}' on '{target_star.name}'")


def _apply_stat_modifiers(star: StarCard, power_card: ModifyStatCard):
    """
    Apply stat modifiers from a ModifyStatCard to a StarCard.

    Args:
        star: The star card to modify
        power_card: The power card with stat modifiers

    Returns:
        None (mutates star object)
    """
    for stat, modifier in power_card.stat_modifiers.items():
        if hasattr(star, stat):
            old_value = getattr(star, stat)
            new_value = old_value + modifier
            setattr(star, stat, new_value)
            logger.info(f"  {star.name}: {stat} {old_value} → {new_value} ({modifier:+d})")
        else:
            logger.warning(f"Star card '{star.name}' has no stat '{stat}'")
