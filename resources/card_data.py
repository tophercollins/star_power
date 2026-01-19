"""
Hardcoded card data for Star Power
Replaces Google Sheets integration for production deployment
"""
import uuid
from typing import List
from engine.models.cards import (
    StarCard, ModifyStatCard, FanCard,
    StatContestEvent
)

def get_star_cards() -> List[StarCard]:
    """Return a list of Star Cards (celebrities/influencers)

    Stat ranges create tier system:
    - Low tier (total 10-16): Rising/struggling artists
    - Mid tier (total 17-26): Solid performers
    - High tier (total 27-40): Icons and legends
    """
    cards = [
        # ===== LEGENDARY TIER (35-40 total) =====
        StarCard(
            id=str(uuid.uuid4()),
            name="Beyoncé",
            aura=10, talent=10, influence=10, legacy=10,
            tags=["Pop", "R&B", "Legend"]
        ),
        StarCard(
            id=str(uuid.uuid4()),
            name="Michael Jackson",
            aura=10, talent=10, influence=10, legacy=10,
            tags=["Pop", "Legend"]
        ),
        StarCard(
            id=str(uuid.uuid4()),
            name="Jay-Z",
            aura=9, talent=8, influence=9, legacy=10,
            tags=["Rapper", "Mogul", "Legend"]
        ),
        StarCard(
            id=str(uuid.uuid4()),
            name="Madonna",
            aura=9, talent=8, influence=9, legacy=10,
            tags=["Pop", "Legend"]
        ),
        StarCard(
            id=str(uuid.uuid4()),
            name="Dolly Parton",
            aura=9, talent=9, influence=7, legacy=10,
            tags=["Country", "Legend"]
        ),

        # ===== HIGH TIER (27-34 total) =====
        StarCard(
            id=str(uuid.uuid4()),
            name="Taylor Swift",
            aura=9, talent=8, influence=9, legacy=8,
            tags=["Pop"]
        ),
        StarCard(
            id=str(uuid.uuid4()),
            name="Kendrick Lamar",
            aura=7, talent=9, influence=8, legacy=7,
            tags=["Rapper"]
        ),
        StarCard(
            id=str(uuid.uuid4()),
            name="Daft Punk",
            aura=8, talent=9, influence=8, legacy=9,
            tags=["DJ", "Producer"]
        ),
        StarCard(
            id=str(uuid.uuid4()),
            name="Drake",
            aura=8, talent=7, influence=8, legacy=6,
            tags=["Rapper", "Pop"]
        ),
        StarCard(
            id=str(uuid.uuid4()),
            name="Shakira",
            aura=8, talent=7, influence=7, legacy=8,
            tags=["Latin", "Pop"]
        ),

        # ===== MID TIER (20-26 total) =====
        StarCard(
            id=str(uuid.uuid4()),
            name="Ariana Grande",
            aura=7, talent=8, influence=7, legacy=5,
            tags=["Pop"]
        ),
        StarCard(
            id=str(uuid.uuid4()),
            name="The Weeknd",
            aura=7, talent=8, influence=7, legacy=5,
            tags=["Pop", "R&B"]
        ),
        StarCard(
            id=str(uuid.uuid4()),
            name="Bruno Mars",
            aura=7, talent=8, influence=6, legacy=5,
            tags=["Pop", "R&B"]
        ),
        StarCard(
            id=str(uuid.uuid4()),
            name="Billie Eilish",
            aura=7, talent=7, influence=7, legacy=4,
            tags=["Pop", "Alternative"]
        ),
        StarCard(
            id=str(uuid.uuid4()),
            name="Bad Bunny",
            aura=7, talent=6, influence=7, legacy=4,
            tags=["Latin", "Rapper"]
        ),
        StarCard(
            id=str(uuid.uuid4()),
            name="Calvin Harris",
            aura=6, talent=7, influence=6, legacy=5,
            tags=["DJ", "Producer"]
        ),
        StarCard(
            id=str(uuid.uuid4()),
            name="SZA",
            aura=6, talent=7, influence=6, legacy=4,
            tags=["R&B"]
        ),
        StarCard(
            id=str(uuid.uuid4()),
            name="Cardi B",
            aura=7, talent=5, influence=7, legacy=3,
            tags=["Rapper", "Pop"]
        ),

        # ===== LOW-MID TIER (15-19 total) =====
        StarCard(
            id=str(uuid.uuid4()),
            name="Post Malone",
            aura=5, talent=5, influence=6, legacy=3,
            tags=["Pop", "Rapper"]
        ),
        StarCard(
            id=str(uuid.uuid4()),
            name="Morgan Wallen",
            aura=5, talent=6, influence=5, legacy=2,
            tags=["Country"]
        ),
        StarCard(
            id=str(uuid.uuid4()),
            name="Ice Spice",
            aura=6, talent=4, influence=6, legacy=2,
            tags=["Rapper"]
        ),
        StarCard(
            id=str(uuid.uuid4()),
            name="Olivia Rodrigo",
            aura=6, talent=6, influence=5, legacy=2,
            tags=["Pop"]
        ),

        # ===== LOW TIER (10-14 total) - Rising/Struggling =====
        StarCard(
            id=str(uuid.uuid4()),
            name="Lil Pump",
            aura=4, talent=3, influence=4, legacy=2,
            tags=["Rapper"]
        ),
        StarCard(
            id=str(uuid.uuid4()),
            name="Bhad Bhabie",
            aura=5, talent=2, influence=4, legacy=1,
            tags=["Rapper"]
        ),
        StarCard(
            id=str(uuid.uuid4()),
            name="Rebecca Black",
            aura=3, talent=4, influence=3, legacy=2,
            tags=["Pop"]
        ),
        StarCard(
            id=str(uuid.uuid4()),
            name="Vanilla Ice",
            aura=4, talent=3, influence=3, legacy=3,
            tags=["Rapper"]
        ),
    ]
    return cards

def get_power_cards() -> List[ModifyStatCard]:
    """Return a list of Power Cards (stat modifiers)"""
    cards = [
        ModifyStatCard(
            id=str(uuid.uuid4()),
            name="Record Deal",
            description="Major label contract boosts talent and influence",
            stat_modifiers={"talent": 2, "influence": 1},
            targets_star=True
        ),
        ModifyStatCard(
            id=str(uuid.uuid4()),
            name="Viral Moment",
            description="Social media fame skyrockets influence",
            stat_modifiers={"influence": 3, "aura": 1},
            targets_star=True
        ),
        ModifyStatCard(
            id=str(uuid.uuid4()),
            name="Award Show Win",
            description="Industry recognition increases legacy and aura",
            stat_modifiers={"legacy": 2, "aura": 2},
            targets_star=True
        ),
        ModifyStatCard(
            id=str(uuid.uuid4()),
            name="Skill Training",
            description="Dedicated practice improves raw talent",
            stat_modifiers={"talent": 3},
            targets_star=True
        ),
        ModifyStatCard(
            id=str(uuid.uuid4()),
            name="PR Campaign",
            description="Marketing push enhances public image",
            stat_modifiers={"aura": 2, "influence": 1},
            targets_star=True
        ),
    ]
    return cards

def get_event_cards():
    """Return a list of Event Cards - SIMPLIFIED to basic single-stat contests only

    Complex event types backed up in card_data_backup_complex_events.py
    """
    cards = [
        # Simple single-stat contests - highest wins
        StatContestEvent(
            id=str(uuid.uuid4()),
            name="Rap Battle",
            description="Who has the best skills?",
            stat_options=["talent"],
            contest_type="highest",
            fan_reward=1
        ),
        StatContestEvent(
            id=str(uuid.uuid4()),
            name="Red Carpet Event",
            description="Who has the most star power?",
            stat_options=["aura"],
            contest_type="highest",
            fan_reward=1
        ),
        StatContestEvent(
            id=str(uuid.uuid4()),
            name="Social Media Battle",
            description="Who has the biggest reach?",
            stat_options=["influence"],
            contest_type="highest",
            fan_reward=1
        ),
        StatContestEvent(
            id=str(uuid.uuid4()),
            name="Hall of Fame",
            description="Who has the greatest legacy?",
            stat_options=["legacy"],
            contest_type="highest",
            fan_reward=1
        ),
        # Duplicate each event type for more variety in the deck
        StatContestEvent(
            id=str(uuid.uuid4()),
            name="Talent Showcase",
            description="Pure skill competition",
            stat_options=["talent"],
            contest_type="highest",
            fan_reward=1
        ),
        StatContestEvent(
            id=str(uuid.uuid4()),
            name="Award Show",
            description="Who shines brightest?",
            stat_options=["aura"],
            contest_type="highest",
            fan_reward=1
        ),
        StatContestEvent(
            id=str(uuid.uuid4()),
            name="Viral Moment",
            description="Who trends harder?",
            stat_options=["influence"],
            contest_type="highest",
            fan_reward=1
        ),
        StatContestEvent(
            id=str(uuid.uuid4()),
            name="Icon Status",
            description="Who's more legendary?",
            stat_options=["legacy"],
            contest_type="highest",
            fan_reward=1
        ),
    ]
    return cards

def get_fan_cards() -> List[FanCard]:
    """Return a list of Fan Cards (victory points)"""
    cards = []

    # Generic fans (10 copies)
    for i in range(10):
        cards.append(
            FanCard(
                id=str(uuid.uuid4()),
                name="Generic Fan",
                bonus=1,
                tag=None
            )
        )

    # Generic superfans (2 copies)
    for i in range(2):
        cards.append(
            FanCard(
                id=str(uuid.uuid4()),
                name="Generic Superfan",
                bonus=2,
                tag=None
            )
        )

    # Tagged fans (2 copies per tag)
    tags = ["Rapper", "Pop", "DJ", "R&B", "Producer", "Alternative", "Latin", "Country", "Legend"]
    for tag in tags:
        for i in range(2):
            cards.append(
                FanCard(
                    id=str(uuid.uuid4()),
                    name=f"{tag} Fan",
                    bonus=1,
                    tag=tag
                )
            )

    # Tagged superfans (1 copy per tag)
    for tag in tags:
        cards.append(
            FanCard(
                id=str(uuid.uuid4()),
                name=f"{tag} Superfan",
                bonus=2,
                tag=tag
            )
        )

    return cards
