from engine.models.cards import StarCard
import logging

logger = logging.getLogger(__name__)

def play_star_from_hand(player, hand_index: int):
    card = player.hand[hand_index]
    if not isinstance(card, StarCard):
        logger.info(f"Cannot play non-star card: {getattr(card, 'name', 'Unknown')}")
        return

    player.hand.pop(hand_index)
    player.star_cards.append(card)
    logger.info(f"{player.name} played {card.name}")