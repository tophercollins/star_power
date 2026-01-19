"""
BACKUP FILE - Complex Event Cards
These event types are stored here for future use.
Currently using simplified single-stat events only.
"""
import uuid
from engine.models.cards import (
    StatContestEvent, CombinedStatEvent, ThresholdEvent,
    TagBasedEvent, RiskRewardEvent, SharedRewardEvent
)

def get_complex_event_cards():
    """All the complex event types - stored for future implementation"""
    cards = [
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
