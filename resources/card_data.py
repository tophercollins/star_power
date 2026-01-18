"""
Hardcoded card data for Star Power
Replaces Google Sheets integration for production deployment
"""
import uuid
from typing import List
from engine.models.cards import StarCard, ModifyStatCard, StatContestEvent, FanCard

def get_star_cards() -> List[StarCard]:
    """Return a list of Star Cards (celebrities/influencers)"""
    cards = [
        # Rappers
        StarCard(
            id=str(uuid.uuid4()),
            name="Drake",
            aura=8, talent=7, influence=9, legacy=6,
            tags=["Rapper", "Pop"]
        ),
        StarCard(
            id=str(uuid.uuid4()),
            name="Kendrick Lamar",
            aura=7, talent=10, influence=8, legacy=8,
            tags=["Rapper"]
        ),
        StarCard(
            id=str(uuid.uuid4()),
            name="Jay-Z",
            aura=9, talent=8, influence=10, legacy=10,
            tags=["Rapper", "Mogul"]
        ),
        StarCard(
            id=str(uuid.uuid4()),
            name="Cardi B",
            aura=9, talent=6, influence=9, legacy=5,
            tags=["Rapper", "Pop"]
        ),

        # Pop Stars
        StarCard(
            id=str(uuid.uuid4()),
            name="Taylor Swift",
            aura=9, talent=8, influence=10, legacy=9,
            tags=["Pop"]
        ),
        StarCard(
            id=str(uuid.uuid4()),
            name="Beyoncé",
            aura=10, talent=10, influence=10, legacy=10,
            tags=["Pop", "R&B"]
        ),
        StarCard(
            id=str(uuid.uuid4()),
            name="Ariana Grande",
            aura=8, talent=9, influence=9, legacy=7,
            tags=["Pop"]
        ),
        StarCard(
            id=str(uuid.uuid4()),
            name="The Weeknd",
            aura=8, talent=9, influence=8, legacy=7,
            tags=["Pop", "R&B"]
        ),

        # DJs/Producers
        StarCard(
            id=str(uuid.uuid4()),
            name="Calvin Harris",
            aura=7, talent=8, influence=8, legacy=7,
            tags=["DJ", "Producer"]
        ),
        StarCard(
            id=str(uuid.uuid4()),
            name="Daft Punk",
            aura=9, talent=10, influence=8, legacy=10,
            tags=["DJ", "Producer"]
        ),

        # Rock/Alternative
        StarCard(
            id=str(uuid.uuid4()),
            name="Billie Eilish",
            aura=9, talent=8, influence=9, legacy=6,
            tags=["Pop", "Alternative"]
        ),
        StarCard(
            id=str(uuid.uuid4()),
            name="Post Malone",
            aura=7, talent=7, influence=8, legacy=6,
            tags=["Pop", "Rapper"]
        ),

        # R&B
        StarCard(
            id=str(uuid.uuid4()),
            name="Bruno Mars",
            aura=8, talent=9, influence=8, legacy=7,
            tags=["Pop", "R&B"]
        ),
        StarCard(
            id=str(uuid.uuid4()),
            name="SZA",
            aura=8, talent=8, influence=8, legacy=6,
            tags=["R&B"]
        ),

        # Legends
        StarCard(
            id=str(uuid.uuid4()),
            name="Madonna",
            aura=10, talent=8, influence=9, legacy=10,
            tags=["Pop", "Legend"]
        ),
        StarCard(
            id=str(uuid.uuid4()),
            name="Michael Jackson",
            aura=10, talent=10, influence=10, legacy=10,
            tags=["Pop", "Legend"]
        ),

        # Latin
        StarCard(
            id=str(uuid.uuid4()),
            name="Bad Bunny",
            aura=9, talent=7, influence=9, legacy=6,
            tags=["Latin", "Rapper"]
        ),
        StarCard(
            id=str(uuid.uuid4()),
            name="Shakira",
            aura=9, talent=8, influence=9, legacy=9,
            tags=["Latin", "Pop"]
        ),

        # Country
        StarCard(
            id=str(uuid.uuid4()),
            name="Morgan Wallen",
            aura=7, talent=7, influence=8, legacy=5,
            tags=["Country"]
        ),
        StarCard(
            id=str(uuid.uuid4()),
            name="Dolly Parton",
            aura=10, talent=9, influence=8, legacy=10,
            tags=["Country", "Legend"]
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

def get_event_cards() -> List[StatContestEvent]:
    """Return a list of Event Cards (stat contests)"""
    cards = [
        # Single stat contests
        StatContestEvent(
            id=str(uuid.uuid4()),
            name="Rap Battle",
            description="Pure lyrical showdown",
            stat_options=["talent"],
            contest_type="single"
        ),
        StatContestEvent(
            id=str(uuid.uuid4()),
            name="Red Carpet Appearance",
            description="Who commands the most presence?",
            stat_options=["aura"],
            contest_type="single"
        ),
        StatContestEvent(
            id=str(uuid.uuid4()),
            name="Social Media Feud",
            description="Battle for online dominance",
            stat_options=["influence"],
            contest_type="single"
        ),
        StatContestEvent(
            id=str(uuid.uuid4()),
            name="Hall of Fame Induction",
            description="Who has the greater lasting impact?",
            stat_options=["legacy"],
            contest_type="single"
        ),

        # Double stat contests
        StatContestEvent(
            id=str(uuid.uuid4()),
            name="Award Show Performance",
            description="Choose: talent or aura",
            stat_options=["talent", "aura"],
            contest_type="double"
        ),
        StatContestEvent(
            id=str(uuid.uuid4()),
            name="Charity Concert",
            description="Choose: influence or legacy",
            stat_options=["influence", "legacy"],
            contest_type="double"
        ),

        # Quad stat contests
        StatContestEvent(
            id=str(uuid.uuid4()),
            name="Celebrity Face-Off",
            description="All-around star power competition",
            stat_options=["aura", "talent", "influence", "legacy"],
            contest_type="quad"
        ),
        StatContestEvent(
            id=str(uuid.uuid4()),
            name="Icon Status Battle",
            description="Who is the bigger star?",
            stat_options=["aura", "talent", "influence", "legacy"],
            contest_type="quad"
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
