# engine/models/cards.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Optional

# ---------- Star Cards ----------

@dataclass
class StarCard:
    name: str
    aura: int
    talent: int
    influence: int
    legacy: int
    tags: List[str] = field(default_factory=list)

    # Zones / attachments (state only; effects handled in rules)
    attached_fans: List[FanCard] = field(default_factory=list)
    attached_power_cards: List[PowerCard] = field(default_factory=list)


# ---------- Event Cards ----------

@dataclass
class EventCard:
    name: str
    description: str = ""


@dataclass
class StatContestEvent(EventCard):
    # e.g. ["aura"] or ["aura", "talent"] or ["aura","talent","influence","legacy"]
    stat_options: List[str] = field(default_factory=list)

    # Store contest kind explicitly (compute in setup/rules if you like)
    # Values could be: "fixed", "choice_of_2", "choice_of_4", "custom"
    contest_type: str = "custom"


# ---------- Fan Cards ----------

@dataclass
class FanCard:
    name: str
    bonus: int
    tag: Optional[str] = None  # e.g. "rapper"


# ---------- Power Cards ----------

@dataclass
class PowerCard:
    name: str
    description: str = "No description provided."
    targets_star: bool = False


@dataclass
class ModifyStatCard(PowerCard):
    # Only non-zero modifiers; enforce/clean in builder or rules layer
    stat_modifiers: Dict[str, int] = field(default_factory=dict)
    # This card attaches to stars
    targets_star: bool = True


@dataclass
class LocationPowerCard(PowerCard):
    # Behavior (apply effects, tie overrides, etc.) will live in rules later
    pass
