"""
Hardcoded card data for Star Power
Replaces Google Sheets integration for production deployment
"""
import uuid
from typing import List
from engine.models.cards import (
    StarCard, ModifyStatCard, FanCard,
    StatContestEvent, CombinedStatEvent, ThresholdEvent,
    TagBasedEvent, RiskRewardEvent, SharedRewardEvent
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
    """Return a list of Event Cards with varied win conditions (Marvel Snap-inspired)"""
    cards = [
        # ===== STAT CONTEST EVENTS (Highest Wins) =====
        StatContestEvent(
            id=str(uuid.uuid4()),
            name="Rap Battle",
            description="Who has the superior skills?",
            stat_options=["talent"],
            contest_type="highest",
            fan_reward=1
        ),
        StatContestEvent(
            id=str(uuid.uuid4()),
            name="Red Carpet Showdown",
            description="Who commands the most presence?",
            stat_options=["aura"],
            contest_type="highest",
            fan_reward=1
        ),
        StatContestEvent(
            id=str(uuid.uuid4()),
            name="Social Media War",
            description="Battle for online dominance",
            stat_options=["influence"],
            contest_type="highest",
            fan_reward=1
        ),
        StatContestEvent(
            id=str(uuid.uuid4()),
            name="Hall of Fame Vote",
            description="Choose: talent or aura",
            stat_options=["talent", "aura"],
            contest_type="highest",
            fan_reward=1
        ),

        # ===== INVERSE CONTESTS (Lowest Wins) =====
        StatContestEvent(
            id=str(uuid.uuid4()),
            name="Rookie Spotlight",
            description="Fresh talent rises! Lowest Legacy wins",
            stat_options=["legacy"],
            contest_type="lowest",
            fan_reward=1
        ),
        StatContestEvent(
            id=str(uuid.uuid4()),
            name="Underdog Story",
            description="The humble triumph! Lowest Aura wins",
            stat_options=["aura"],
            contest_type="lowest",
            fan_reward=1
        ),

        # ===== COMBINED STAT EVENTS =====
        CombinedStatEvent(
            id=str(uuid.uuid4()),
            name="Total Star Power",
            description="Sum of ALL stats determines the winner",
            required_stats=["aura", "talent", "influence", "legacy"],
            fan_reward=2
        ),
        CombinedStatEvent(
            id=str(uuid.uuid4()),
            name="Skill + Charisma",
            description="Talent + Aura combined",
            required_stats=["talent", "aura"],
            fan_reward=1
        ),
        CombinedStatEvent(
            id=str(uuid.uuid4()),
            name="Impact + Legacy",
            description="Influence + Legacy combined",
            required_stats=["influence", "legacy"],
            fan_reward=1
        ),

        # ===== THRESHOLD EVENTS =====
        ThresholdEvent(
            id=str(uuid.uuid4()),
            name="Elite Club",
            description="Must have Influence 7+ to enter. Highest Aura wins",
            required_stat="influence",
            threshold=7,
            winning_stat="aura",
            fan_reward=2
        ),
        ThresholdEvent(
            id=str(uuid.uuid4()),
            name="Veteran's Tournament",
            description="Must have Legacy 6+ to compete. Highest Talent wins",
            required_stat="legacy",
            threshold=6,
            winning_stat="talent",
            fan_reward=2
        ),
        ThresholdEvent(
            id=str(uuid.uuid4()),
            name="Main Stage Only",
            description="Must have Aura 6+ to perform. Highest Talent wins",
            required_stat="aura",
            threshold=6,
            winning_stat="talent",
            fan_reward=2
        ),

        # ===== TAG-BASED EVENTS =====
        TagBasedEvent(
            id=str(uuid.uuid4()),
            name="Hip-Hop Summit",
            description="Rappers only! Highest Influence wins",
            required_tags=["Rapper"],
            winning_stat="influence",
            fan_reward=2
        ),
        TagBasedEvent(
            id=str(uuid.uuid4()),
            name="Pop Music Awards",
            description="Pop stars only! Highest Aura wins",
            required_tags=["Pop"],
            winning_stat="aura",
            fan_reward=2
        ),
        TagBasedEvent(
            id=str(uuid.uuid4()),
            name="Legend's Ceremony",
            description="Legends only! Highest Legacy wins",
            required_tags=["Legend"],
            winning_stat="legacy",
            fan_reward=3
        ),
        TagBasedEvent(
            id=str(uuid.uuid4()),
            name="DJ Battle",
            description="DJs only! Highest Talent wins",
            required_tags=["DJ"],
            winning_stat="talent",
            fan_reward=2
        ),

        # ===== RISK/REWARD EVENTS =====
        RiskRewardEvent(
            id=str(uuid.uuid4()),
            name="Viral Challenge",
            description="High stakes! Winner gets 3 fans, loser loses 1",
            stat_options=["influence"],
            fan_reward=3,
            fan_penalty=1
        ),
        RiskRewardEvent(
            id=str(uuid.uuid4()),
            name="Career-Defining Moment",
            description="Everything on the line! Choose any stat",
            stat_options=["aura", "talent", "influence", "legacy"],
            fan_reward=3,
            fan_penalty=1
        ),
        RiskRewardEvent(
            id=str(uuid.uuid4()),
            name="Controversial Feud",
            description="High risk! Choose: Aura or Influence",
            stat_options=["aura", "influence"],
            fan_reward=2,
            fan_penalty=1
        ),

        # ===== SHARED REWARD EVENTS =====
        SharedRewardEvent(
            id=str(uuid.uuid4()),
            name="Charity Concert",
            description="Both stars gain fans! Winner: 2, Runner-up: 1",
            stat_options=["talent", "aura"],
            winner_fans=2,
            loser_fans=1
        ),
        SharedRewardEvent(
            id=str(uuid.uuid4()),
            name="Collaboration Event",
            description="Everyone wins! Highest Influence gets 3, other gets 1",
            stat_options=["influence"],
            winner_fans=3,
            loser_fans=1
        ),
        SharedRewardEvent(
            id=str(uuid.uuid4()),
            name="Industry Celebration",
            description="All participants rewarded! Choose any stat",
            stat_options=["aura", "talent", "influence", "legacy"],
            winner_fans=2,
            loser_fans=1
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
