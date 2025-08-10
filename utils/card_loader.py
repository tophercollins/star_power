from typing import List
import uuid
from engine.models.cards import (
    StarCard,
    StatContestEvent,
    FanCard,
    PowerCard,            # if you later load power cards
    ModifyStatCard,       # optional
)

def _new_id():
    return str(uuid.uuid4())

def load_star_cards(sheet):
    rows = sheet.get_all_records()
    stars = []

    for row in rows:
        stars.append(
            StarCard(
                id=_new_id(),
                name=row["Name"],
                aura=int(row["Aura"]),
                talent=int(row["Talent"]),
                influence=int(row["Influence"]),
                legacy=int(row["Legacy"]),
                tags=[t.strip() for t in row.get("Tags", "").split(",") if t.strip()]
            )
        )
    return stars

def load_power_cards(sheet):
    rows = sheet.get_all_records()
    powers = []

    for row in rows:
        if row.get("Type") == "Modify Stat":
            powers.append(
                ModifyStatCard(
                    id=_new_id(),
                    name=row.get("Name", "Unnamed Power"),
                    description=row.get("Description", ""),
                    targets_star=True,
                    stat_modifiers={
                        "aura": int(row.get("Aura Mod", 0)),
                        "talent": int(row.get("Talent Mod", 0)),
                        "influence": int(row.get("Influence Mod", 0)),
                        "legacy": int(row.get("Legacy Mod", 0)),
                        }
                    )
            )
        else:
            pass  # Skip unsupported power card types for now
    return powers

def load_event_cards(sheet):
    rows = sheet.get_all_records()
    events = []
    for row in rows:
        if row.get("Type") == "Stat Contest":
            events.append(
                StatContestEvent(
                    id=_new_id(),
                    name=row["Name"], 
                    stat_options=[s.strip() for s in row["Stat Options"].split(",")]
                    )
                )
        else:
            print(f"Skipping unknown event type: {row}")
    return events

def load_fan_cards(sheet):
    rows = sheet.get_all_records()
    fans = []
    for row in rows:
        fans.append(
            FanCard(
                id=_new_id(),
                name=row.get("Name"),
                bonus=int(row.get("Bonus")),
                tag=row.get("Tag") or None
            )
        )
    return fans