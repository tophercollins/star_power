from engine.models.cards import StarCard

def play_star_from_hand(player, hand_index: int, log: list):
    card = player.hand[hand_index]
    if not isinstance(card, StarCard):
        log.append(f"Cannot play non-star card: {getattr(card, 'name', 'Unknown')}")
        return

    player.hand.pop(hand_index)
    player.star_cards.append(card)
    log.append(f"{player.name} played {card.name}")