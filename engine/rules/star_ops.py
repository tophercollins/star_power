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
    logger.info(f"play_star_from_hand called: player={player.name}, hand_index={hand_index}, replace_star_index={replace_star_index}, discard_pile={'present' if discard_pile is not None else 'None'}")
    logger.info(f"Player hand size before: {len(player.hand)}, board size before: {len(player.star_cards)}")

    card = player.hand[hand_index]
    if not isinstance(card, StarCard):
        logger.info(f"Cannot play non-star card: {getattr(card, 'name', 'Unknown')}")
        return

    logger.info(f"Card to play: {card.name}")

    # Remove card from hand
    logger.info(f"Removing card from hand at index {hand_index}")
    player.hand.pop(hand_index)
    logger.info(f"Hand size after removal: {len(player.hand)}")

    # If replacing a star on board
    if replace_star_index is not None:
        logger.info(f"Replacement mode: replacing star at board index {replace_star_index}")
        logger.info(f"Board before replacement: {[s.name for s in player.star_cards]}")
        replaced_star = player.star_cards.pop(replace_star_index)
        logger.info(f"Replaced star: {replaced_star.name}")
        if discard_pile is not None:
            discard_pile.append(replaced_star)
            logger.info(f"Added {replaced_star.name} to discard pile")
        logger.info(f"{player.name} replaced {replaced_star.name} with {card.name} (discarded)")

    # Add new star to board
    logger.info(f"Adding {card.name} to board")
    player.star_cards.append(card)
    logger.info(f"Board after: {[s.name for s in player.star_cards]}")
    logger.info(f"{player.name} played {card.name}")