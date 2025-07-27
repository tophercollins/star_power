
class Board:
    def __init__(self, players):
        """
        players: list of Player objects
        """
        self.players = players
        self.star_zone = {player.name: [] for player in players}  # current stars in play

    def play_star(self, player, star_card):
        self.star_zone[player.name].append(star_card)

    def get_played_stars(self, player):
        return self.star_zone.get(player.name, [])
    
    def show_board(self):
        for player in self.players:
            cards = self.cards_in_play.get(player.name, [])

    def reset(self):
        """Clear board state if needed between rounds or games."""
        self.star_zone = {name: [] for name in self.star_zone}

    def __str__(self):
        out = []
        for player in self.players:
            stars = self.star_zone[player.name]
            out.append(f"{player.name}: {[s.name for s in stars]}")
        return "\n".join(out)
