# engine/models/player.py
from dataclasses import dataclass, field
from typing import List, Any

@dataclass
class Player:
    name: str
    is_human: bool = True

    # Zones
    hand: List[Any] = field(default_factory=list)
    star_cards: List[Any] = field(default_factory=list)
    locations: List[Any] = field(default_factory=list)
