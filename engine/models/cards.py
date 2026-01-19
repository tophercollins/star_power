from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import uuid

@dataclass
class StarCard:
    id: str
    name: str
    aura: int
    talent: int
    influence: int
    legacy: int
    tags: List[str] = field(default_factory=list)
    attached_fans: List[FanCard] = field(default_factory=list)
    attached_power_cards: List[PowerCard] = field(default_factory=list)


@dataclass
class EventCard:
    id: str
    name: str
    description: str = ""
    event_type: str = "basic"  # Type of event for resolution logic
    fan_reward: int = 1  # How many fans the winner gets


@dataclass
class StatContestEvent(EventCard):
    """Standard event - highest stat wins"""
    stat_options: List[str] = field(default_factory=list)  # Stats players can choose from
    contest_type: str = "highest"  # "highest" or "lowest"
    event_type: str = "stat_contest"


@dataclass
class CombinedStatEvent(EventCard):
    """Event where multiple stats are summed together"""
    required_stats: List[str] = field(default_factory=list)  # Stats to sum
    event_type: str = "combined_stat"


@dataclass
class ThresholdEvent(EventCard):
    """Event requiring minimum stat value to participate"""
    required_stat: str = "aura"
    threshold: int = 5  # Minimum stat value required
    winning_stat: str = "talent"  # Stat used to determine winner among qualified
    event_type: str = "threshold"


@dataclass
class TagBasedEvent(EventCard):
    """Event where only certain tags can participate"""
    required_tags: List[str] = field(default_factory=list)  # Tags that can compete
    winning_stat: str = "aura"  # Stat used to determine winner
    event_type: str = "tag_based"


@dataclass
class RiskRewardEvent(EventCard):
    """High stakes event with bigger rewards and penalties"""
    stat_options: List[str] = field(default_factory=list)
    fan_reward: int = 2  # Winner gets more fans
    fan_penalty: int = 1  # Loser loses fans
    event_type: str = "risk_reward"


@dataclass
class SharedRewardEvent(EventCard):
    """Both players receive fans based on participation"""
    stat_options: List[str] = field(default_factory=list)
    winner_fans: int = 2
    loser_fans: int = 1
    event_type: str = "shared_reward"


@dataclass
class FanCard:
    id: str
    name: str
    bonus: int
    tag: Optional[str] = None


@dataclass
class PowerCard:
    id: str
    name: str
    description: str = ""
    targets_star: bool = False


@dataclass
class ModifyStatCard(PowerCard):
    stat_modifiers: Dict[str, int] = field(default_factory=dict)
    targets_star: bool = True


@dataclass
class LocationPowerCard(PowerCard):
    pass
