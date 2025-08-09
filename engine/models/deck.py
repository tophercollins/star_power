from dataclasses import dataclass, field
from typing import List, Any

@dataclass
class Deck:
    name: str
    cards: List[Any] = field(default_factory=list)