from resources.config import GAME_CONFIG
from classes.player_classes import HumanPlayer, ComputerPlayer
from classes.deck_classes import MainDeck, EventDeck
from classes.board_classes import Board

class Game:
    def __init__(self):
        self.players = [HumanPlayer("You"), ComputerPlayer("AI")]
        self.main_deck = MainDeck()
        self.event_deck = EventDeck()
        self.board = Board(self.players)
        self.turn = 1
        self.contest_start_turn = 2
        self.fans_to_win = GAME_CONFIG["fans_to_win"]
        self.draw_starting_hands()

    def draw_starting_hands(self):
        hand_size = GAME_CONFIG["starting_hand_size"]
        for player in self.players:
            print(f"\n🎴 {player.name} draws {hand_size} starting card(s).")
            for _ in range(hand_size):
                card = self.main_deck.draw()
                player.hand.append(card)

    def run(self):
        while True:
            print(f"\n🌀 Turn {self.turn}")

            for player in self.players:
                if self.play_turn(player):
                    self.end_game()
                    return

            if self.turn >= self.contest_start_turn:
                self.run_contest()

            self.turn += 1

    def play_turn(self, player):
        print(f"\n{player.name}'s Turn")

        for _ in range(GAME_CONFIG["cards_drawn_per_turn"]):
            card = self.main_deck.draw()
            if not card:
                print("⚠️ Main deck is empty.")
                return True
            player.hand.append(card)
            print(f"{player.name} drew: {card.name}")

        player.play_star_from_hand()
        return False

    def run_contest(self):
        print("\n⚔️ Contest Time!")

        human, ai = self.players

        human_star = human.choose_star_for_contest()
        ai_star = ai.choose_star_for_contest()

        if not human_star or not ai_star:
            print("Not enough stars in play to contest.")
            return

        event = self.event_deck.draw()
        print(f"\n🃏 Event: {event.name} ({event.type})")
        print(event.description)

        if event.type != "fixed":
            print(f"Stat options: {event.stat_options}")
            while True:
                stat = input("Choose a stat for the contest: ").lower()
                if stat in event.stat_options:
                    break
                print("Invalid stat. Try again.")
            winners = event.resolve([human_star, ai_star], chosen_stat=stat)
        else:
            winners = event.resolve([human_star, ai_star])

        if len(winners) == 1:
            winner = winners[0]
            winner_player = human if winner == human_star else ai
            winner_player.fans += 1
            print(f"\n🏆 {winner_player.name} wins and earns 1 fan!")
        else:
            print("\n🤝 It's a tie — both players gain 1 fan!.")
            for player in self.players:
                player.fans += 1

    def end_game(self):
        print("\n🏁 Game Over!")
        for player in self.players:
            print(f"{player.name} - Fans: {player.fans}")

        p1, p2 = self.players
        if p1.fans > p2.fans:
            print("🎉 You win!")
        elif p1.fans < p2.fans:
            print("💀 AI wins!")
        else:
            print("🤝 It's a draw!")
