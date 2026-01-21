"""
Power Card Operations - Playing power cards and applying stat modifications
"""
import logging
from engine.models.cards import PowerCard, ModifyStatCard, StealStarCard, StarCard

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


def steal_star_from_opponent(
    stealing_player,
    victim_player,
    hand_index: int,
    opponent_star_index: int,
    sacrifice_star_index: int = None,
    discard_pile: list = None
):
    """
    Play a StealStarCard to steal an opponent's star with all attachments.

    Args:
        stealing_player: The player stealing the star
        victim_player: The opponent losing the star
        hand_index: Index of StealStarCard in stealing player's hand
        opponent_star_index: Index of star to steal from opponent's board
        sacrifice_star_index: Index of own star to sacrifice if board is full
        discard_pile: List to add sacrificed star to

    Returns:
        None (mutates both players' states)
    """
    logger.info(f"steal_star_from_opponent called: stealer={stealing_player.name}, victim={victim_player.name}, "
                f"hand_index={hand_index}, opponent_star_index={opponent_star_index}, sacrifice_star_index={sacrifice_star_index}")

    # Validate hand index
    if hand_index is None or hand_index < 0 or hand_index >= len(stealing_player.hand):
        logger.warning(f"Invalid hand index: {hand_index}")
        return

    card = stealing_player.hand[hand_index]

    # Validate it's a steal card
    if not isinstance(card, StealStarCard):
        logger.warning(f"Card at index {hand_index} is not a StealStarCard: {type(card).__name__}")
        return

    # Validate opponent has stars
    if len(victim_player.star_cards) == 0:
        logger.warning(f"{victim_player.name} has no stars to steal")
        return

    # Validate opponent star index
    if opponent_star_index is None or opponent_star_index < 0 or opponent_star_index >= len(victim_player.star_cards):
        logger.warning(f"Invalid opponent star index: {opponent_star_index}")
        return

    # Get the star being stolen
    stolen_star = victim_player.star_cards[opponent_star_index]
    fan_count = len(stolen_star.attached_fans)
    power_count = len(stolen_star.attached_power_cards)

    logger.info(f"Stealing {stolen_star.name} from {victim_player.name} ({fan_count} fans, {power_count} powers)")

    # Check if stealing player's board is full
    from resources.config import GAME_CONFIG
    max_stars = GAME_CONFIG["max_stars_on_board"]

    if len(stealing_player.star_cards) >= max_stars:
        # Board is full - must sacrifice a star
        if sacrifice_star_index is None:
            logger.warning(f"{stealing_player.name}'s board is full but no sacrifice_star_index provided")
            return

        if sacrifice_star_index < 0 or sacrifice_star_index >= len(stealing_player.star_cards):
            logger.warning(f"Invalid sacrifice_star_index: {sacrifice_star_index}")
            return

        # Sacrifice own star
        sacrificed_star = stealing_player.star_cards.pop(sacrifice_star_index)
        sacrificed_fan_count = len(sacrificed_star.attached_fans)

        if discard_pile is not None:
            discard_pile.append(sacrificed_star)

        logger.info(f"{stealing_player.name} sacrificed {sacrificed_star.name} ({sacrificed_fan_count} fans) to make room")

    # Transfer star from victim to stealer
    victim_player.star_cards.pop(opponent_star_index)
    stealing_player.star_cards.append(stolen_star)

    # Remove steal card from hand
    stealing_player.hand.pop(hand_index)

    logger.info(f"⚡ {stealing_player.name} used '{card.name}' to steal {stolen_star.name} from {victim_player.name}!")
    logger.info(f"  Stolen star has {fan_count} fans and {power_count} power cards attached")
