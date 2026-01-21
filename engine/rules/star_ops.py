from engine.models.cards import StarCard
import logging

logger = logging.getLogger(__name__)

def play_star_from_hand(player, hand_index: int, replace_star_index: int = None, discard_pile: list = None):
    """
    Play a star card from hand, optionally replacing a star on the board.

    Args:
        player: The player object
        hand_index: Index of card in hand
        replace_star_index: If board is full, index of star to replace
        discard_pile: List to add replaced stars to
    """
    card = player.hand[hand_index]
    if not isinstance(card, StarCard):
        logger.info(f"Cannot play non-star card: {getattr(card, 'name', 'Unknown')}")
        return

    # Remove card from hand
    player.hand.pop(hand_index)

    # If replacing a star on board
    if replace_star_index is not None:
        replaced_star = player.star_cards.pop(replace_star_index)
        if discard_pile is not None:
            discard_pile.append(replaced_star)
        logger.info(f"{player.name} replaced {replaced_star.name} with {card.name} (discarded)")

    # Add new star to board
    player.star_cards.append(card)
    logger.info(f"{player.name} played {card.name}")