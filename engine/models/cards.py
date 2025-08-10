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


@dataclass
class StatContestEvent(EventCard):
    stat_options: List[str] = field(default_factory=list)
    contest_type: str = "custom"


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
