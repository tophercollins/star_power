
# Star Cards
class StarCard:
    def __init__(self, name, aura, talent, influence, legacy, tags=None):
        """
        tags: Optional list like ['rapper', 'pop star']
        """
        self.name = name
        self.aura = aura
        self.talent = talent
        self.influence = influence
        self.legacy = legacy
        self.tags = tags or []

    def __str__(self):
        tag_str = f" ({', '.join(self.tags)})" if self.tags else ""
        return (
            f"{self.name}{tag_str} | "
            f"Aura: {self.aura}, Talent: {self.talent}, "
            f"Influence: {self.influence}, Legacy: {self.legacy}"
        )

    def get_stat(self, stat_name):
        return getattr(self, stat_name, None)

# Event Cards
class EventCard:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description

    def resolve(self, stars):
        """
        Should be implemented by child classes.
        stars: list of StarCard instances.
        """
        raise NotImplementedError("resolve() must be implemented by subclasses")

    def __str__(self):
        return f"{self.name} - {self.description}"

class StatContestEvent(EventCard):
    def __init__(self, name, stat_options, description=None):
        """
        stat_options: list of allowed stats for this contest
        """
        self.stat_options = [s.lower() for s in stat_options]

        # Auto-determine contest type
        if len(self.stat_options) == 1:
            self.type = "fixed"
        elif len(self.stat_options) == 2:
            self.type = "choice_of_2"
        elif len(self.stat_options) == 4:
            self.type = "choice_of_4"
        else:
            self.type = "custom"

        desc = description or self._default_description()
        super().__init__(name, desc)

    def _default_description(self):
        if self.type == "fixed":
            return f"Contest based on {self.stat_options[0].capitalize()}"
        else:
            options = " / ".join(s.capitalize() for s in self.stat_options)
            return f"Choose one stat to compete in: {options}"

    def resolve(self, stars, chosen_stat=None):
        """
        stars: list of StarCard objects
        chosen_stat: required if event type allows choice
        """
        if not self.stat_options:
            raise ValueError("No stats defined for contest.")

        if self.type == "fixed":
            stat = self.stat_options[0]
        else:
            if not chosen_stat:
                raise ValueError("Must provide a stat choice for this event.")
            if chosen_stat.lower() not in self.stat_options:
                raise ValueError(f"{chosen_stat} is not a valid stat for this contest.")
            stat = chosen_stat.lower()

        max_value = max(star.get_stat(stat) for star in stars)
        winners = [star for star in stars if star.get_stat(stat) == max_value]
        return winners
