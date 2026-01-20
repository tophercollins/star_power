"""
Event Operations - Event triggering, star selection, and contest resolution
"""
import logging
from typing import Dict, Any, Optional, Tuple, List
from engine.models.cards import (
    EventCard, StatContestEvent, StarCard, FanCard
    # Complex event types removed - see card_data_backup_complex_events.py
    # CombinedStatEvent, ThresholdEvent, TagBasedEvent, RiskRewardEvent, SharedRewardEvent
)
from engine.models.deck import Deck
from engine.rules.deck_ops import draw_card

logger = logging.getLogger(__name__)


def draw_event(event_deck: Deck) -> Optional[EventCard]:
    """
    Draw an event card from the event deck.

    Args:
        event_deck: The event deck

    Returns:
        EventCard or None if deck is empty
    """
    card = draw_card(event_deck)
    if card:
        logger.info(f"Event drawn: {card.name}")
    return card


def can_star_participate(star: StarCard, event: EventCard) -> Tuple[bool, str]:
    """
    Check if a star can participate in an event.
    Checks if star is exhausted from previous event.

    Args:
        star: The star card
        event: The event card

    Returns:
        Tuple of (can_participate, reason)
    """
    # Check if star is exhausted
    if star.exhausted:
        return False, f"{star.name} is exhausted from the previous event"

    return True, "Star can participate"


def calculate_star_score(star: StarCard, event: EventCard, chosen_stat: Optional[str] = None) -> int:
    """
    Calculate a star's score for an event.
    Simplified - all events are basic stat contests.

    Args:
        star: The star card
        event: The event card
        chosen_stat: The stat chosen by the player

    Returns:
        The star's score for this event
    """
    # All events are StatContestEvent - use chosen stat
    if not chosen_stat:
        logger.warning("StatContestEvent requires chosen_stat")
        return 0
    return getattr(star, chosen_stat, 0)


def resolve_event(
    event: EventCard,
    player1_star: Optional[StarCard],
    player2_star: Optional[StarCard],
    player1_stat: Optional[str],
    player2_stat: Optional[str],
    fan_deck: Deck
) -> Dict[str, Any]:
    """
    Resolve an event and determine the outcome.

    Args:
        event: The event card
        player1_star: Player 1's chosen star (None if no participation)
        player2_star: Player 2's chosen star (None if no participation)
        player1_stat: Player 1's chosen stat (for stat contest events)
        player2_stat: Player 2's chosen stat (for stat contest events)
        fan_deck: The fan deck to draw from

    Returns:
        Dictionary with resolution results:
        {
            "winner": 0 or 1 or None (tie),
            "player1_score": int,
            "player2_score": int,
            "player1_fans_won": int,
            "player2_fans_won": int,
            "player1_fans_lost": int,
            "player2_fans_lost": int,
            "description": str
        }
    """
    result = {
        "winner": None,
        "player1_score": 0,
        "player2_score": 0,
        "player1_fans_won": 0,
        "player2_fans_won": 0,
        "player1_fans_lost": 0,
        "player2_fans_lost": 0,
        "description": ""
    }

    # Check participation
    player1_participates = player1_star is not None
    player2_participates = player2_star is not None

    if not player1_participates and not player2_participates:
        result["description"] = "No players participated in the event"
        return result

    # Calculate scores for participating players
    if player1_participates:
        can_participate, reason = can_star_participate(player1_star, event)
        if can_participate:
            result["player1_score"] = calculate_star_score(player1_star, event, player1_stat)
        else:
            logger.info(f"Player 1's star cannot participate: {reason}")
            player1_participates = False

    if player2_participates:
        can_participate, reason = can_star_participate(player2_star, event)
        if can_participate:
            result["player2_score"] = calculate_star_score(player2_star, event, player2_stat)
        else:
            logger.info(f"Player 2's star cannot participate: {reason}")
            player2_participates = False

    # Only one player participated - they win by default
    if player1_participates and not player2_participates:
        result["winner"] = 0
        result["player1_fans_won"] = getattr(event, 'fan_reward', 1)
        result["description"] = f"Player 1 wins by default ({player1_star.name})"
        return result

    if player2_participates and not player1_participates:
        result["winner"] = 1
        result["player2_fans_won"] = getattr(event, 'fan_reward', 1)
        result["description"] = f"Player 2 wins by default ({player2_star.name})"
        return result

    # Both players participated - compare scores
    p1_score = result["player1_score"]
    p2_score = result["player2_score"]

    # All events are "highest" wins (contest_type="highest")
    # Determine winner
    if p1_score > p2_score:
        result["winner"] = 0
    elif p2_score > p1_score:
        result["winner"] = 1
    else:
        result["winner"] = None  # Tie

    # Standard reward - winner gets 1 fan
    if result["winner"] == 0:
        result["player1_fans_won"] = getattr(event, 'fan_reward', 1)
        winner_star = player1_star
        result["description"] = f"{event.name}: {winner_star.name} wins with {p1_score} {player1_stat}!"
    elif result["winner"] == 1:
        result["player2_fans_won"] = getattr(event, 'fan_reward', 1)
        winner_star = player2_star
        result["description"] = f"{event.name}: {winner_star.name} wins with {p2_score} {player2_stat}!"
    else:
        result["description"] = f"{event.name}: It's a tie! Both have {p1_score} {player1_stat}!"

    logger.info(f"Event resolved: {result['description']}")
    logger.info(f"Scores - P1: {result['player1_score']}, P2: {result['player2_score']}")

    # Mark participating stars as exhausted
    if player1_participates and player1_star:
        player1_star.exhausted = True
        logger.info(f"{player1_star.name} is now exhausted")
    if player2_participates and player2_star:
        player2_star.exhausted = True
        logger.info(f"{player2_star.name} is now exhausted")

    return result


def award_fans(player, fan_deck: Deck, count: int) -> List[FanCard]:
    """
    Draw fan cards from the fan deck and award to player.

    Args:
        player: The player to award fans to
        fan_deck: The fan deck
        count: Number of fans to draw

    Returns:
        List of fan cards drawn
    """
    fans_drawn = []
    for _ in range(count):
        fan = draw_card(fan_deck)
        if fan:
            fans_drawn.append(fan)
            # TODO: Implement fan attachment to stars
            logger.info(f"Fan drawn for {player.name}: {fan.name}")

    return fans_drawn


def remove_fans(player, count: int) -> int:
    """
    Remove fans from a player (for penalty events).

    Args:
        player: The player to remove fans from
        count: Number of fans to remove

    Returns:
        Number of fans actually removed
    """
    # TODO: Implement fan removal from player's stars
    logger.info(f"Removing {count} fans from {player.name}")
    return 0  # Placeholder


def count_player_fans(player) -> int:
    """
    Count total fan points for a player.

    Args:
        player: The player

    Returns:
        Total fan points
    """
    total = 0
    for star in player.star_cards:
        for fan in star.attached_fans:
            total += fan.bonus
    return total
