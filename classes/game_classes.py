from resources.config import GAME_CONFIG
from classes.player_classes import HumanPlayer, ComputerPlayer
from classes.board_classes import Board
from utils.deck_builder import build_decks

class Game:
    def __init__(self):
        self.players = [HumanPlayer("Human 1"), ComputerPlayer("Computer 1")]
        self.main_deck, self.event_deck, self.fan_deck = build_decks()
        self.board = Board(self.players)
        self.discard_pile = []
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
                print(f"{player.name}'s Fans: {player.fans}")

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

        
        print(f"\n{player.name}'s Hand:")
        for card in player.hand:
            print(card)

        print(f"\n{player.name}'s Stars:")
        for card in player.star_cards:
            print(f"{card}")

        player.play_star_from_hand()
        return False

    def run_contest(self):
        print("\n⚔️ Contest Time!")

        human, ai = self.players

        for player in self.players:
            print(f"\n{player.name}'s Stars:")
            for card in player.star_cards:
                print(card)

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
            # Draw a fan card and attach to the winning star
            fan_card = self.fan_deck.draw()
            if fan_card:
                winner.attached_fans.append(fan_card)
                print(f"\n🏆 {winner_player.name} wins and their star {winner.name} gains a fan: {fan_card.name} (+{fan_card.bonus})!")
            else:
                print("\n🏆 {winner_player.name} wins but there are no more fan cards to draw!")
        else:
            print("\n🤝 It's a tie — both players gain a fan card for their contesting star!")
            for star, player in zip([human_star, ai_star], [human, ai]):
                fan_card = self.fan_deck.draw()
                if fan_card:
                    star.attached_fans.append(fan_card)
                    print(f"{player.name}'s star {star.name} gains a fan: {fan_card.name} (+{fan_card.bonus})")
                else:
                    print(f"{player.name} would gain a fan, but the fan deck is empty.")

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