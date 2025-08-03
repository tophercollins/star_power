from classes.card_classes import StarCard, StatContestEvent, FanCard

def load_star_cards(sheet):
    rows = sheet.get_all_records()
    stars = []

    for row in rows:
        tags = [t.strip() for t in row.get("Tags", "").split(",") if t.strip()]
        star = StarCard(
            name=row["Name"],
            aura=int(row["Aura"]),
            talent=int(row["Talent"]),
            influence=int(row["Influence"]),
            legacy=int(row["Legacy"]),
            tags=tags
        )
        stars.append(star)
    return stars

def load_event_cards(sheet):
    rows = sheet.get_all_records()
    events = []

    for row in rows:
        if row.get("Type") == "Stat Contest":
            stat_options = [s.strip() for s in row["Stat Options"].split(",")]
            events.append(StatContestEvent(name=row["Name"], stat_options=stat_options))
        else:
            print(f"Skipping unknown event type: {row}")
    return events

def load_fan_cards(sheet):
    rows = sheet.get_all_records()
    fans = []

    for row in rows:
        name = row.get("Name")
        bonus = int(row.get("Bonus"))
        tag = row.get("Tag") or None

        fan = FanCard(
            name=name,
            bonus=bonus,
            tag=tag
        )
        fans.append(fan)

    return fans