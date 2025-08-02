from resources.config import GAME_CONFIG
from classes.player_classes import Player
from classes.card_classes import StarCard, PowerCard, StatContestEvent
from utils.deck_builder import build_decks

class Game:
    def __init__(self):
        self.players = self.setup_players()
        self.main_deck, self.event_deck, self.fan_deck = build_decks()
        self.discard_pile = []
        self.turn = 1
        self.event_start_turn = GAME_CONFIG["event_start_turn"]
        self.fans_to_win = GAME_CONFIG["fans_to_win"]
        self.draw_starting_hands()

    def setup_players(self):
        human_player_count = int(input("Enter number of human players (1-2): ").strip())
        if human_player_count < 1 or human_player_count > 2:
            raise ValueError("Invalid number of players. Must be 1 or 2.")
        
        players = []
        for i in range(human_player_count):
            name = input(f"Enter name for Player {i + 1}: ")
            players.append(Player(name, is_human=True))
        
        computer_player_count = int(input("Enter number of computer players (0-1): ").strip())
        if computer_player_count < 0 or computer_player_count > 1:
            raise ValueError("Invalid number of computer players. Must be 0 or 1.")
        for i in range(computer_player_count):
            players.append(Player(f"AI Player {i + 1}", is_human=False))

        if len(players) < 2:
            raise ValueError("At least 2 players required.")

        return players
    
    def draw_starting_hands(self):
        hand_size = GAME_CONFIG["starting_hand_size"]
        for player in self.players:
            print(f"\n{player.name} draws {hand_size} starting card(s).")
            for _ in range(hand_size):
                card = self.main_deck.draw()
                player.hand.append(card)

    def run(self):
        while True:
            print(f"\nTurn {self.turn}")

            for player in self.players:
                if self.play_turn(player):
                    self.end_game()
                    return

            self.turn += 1

    def play_turn(self, player):
        print(f"\n{player.name}'s Turn")

        card_draw_limit = GAME_CONFIG["cards_drawn_per_turn"]
        for _ in range(card_draw_limit):
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

        # Action phase
        
        # Play star cards
        star_card_limit = GAME_CONFIG["star_cards_per_turn_limit"]
        for _ in range(star_card_limit):
            options = [card for card in player.hand if isinstance(card, StarCard)]
            if options:
                star_card = player.choose(options=options, prompt="Choose a Star to play:", allow_skip=True)
            else:
                star_card = None
            if star_card:
                player.play_card(star_card, player.star_cards)

        # Play power cards
        power_card_limit = GAME_CONFIG["power_cards_per_turn_limit"]
        for _ in range(power_card_limit):
            options = [card for card in player.hand if isinstance(card, PowerCard)]
            if options:
                power_card = player.choose(options=options, prompt="Choose a Power Card to play:", allow_skip=True)
            else:
                power_card = None
            if power_card:
                if power_card.targets_star:
                    target_star = player.choose(options=player.star_cards, prompt="Choose a Star to attach this Power Card to:", allow_skip=False)
                    player.play_card(power_card, target_star.attached_power_cards)
                else:
                    # TODO: Add logic for other power card types
                    pass

        # Event phase
        if self.turn >= self.event_start_turn:
            event_card = self.event_deck.draw()
            if not event_card:
                print("⚠️ Event deck is empty. No event this turn.")
            else:
                if isinstance(event_card, StatContestEvent):
                    self.run_contest(event_card, player)
                else:
                    # TODO: Handle other event types
                    pass
        
        return False

    def run_contest(self, event, player_turn):
        print("\n⚔️ Contest Time!")

        print(f"\n🃏 Event: {event.name} ({event.type})")
        print(event.description)

        star_selections = []

        for player in self.players:
            print(f"\n{player.name}'s Stars:")
            for card in player.star_cards:
                print(card)
            star_card = player.choose(options=player.star_cards, prompt="Choose a Star to contest with:", allow_skip=False)
            star_selections.append(star_card)

        if event.type != "fixed":
            print(f"Stat options: {event.stat_options}")
            stat = player_turn.choose(options=event.stat_options, prompt="Choose a stat for the contest:", allow_skip=False)
            winners = event.resolve(star_selections, chosen_stat=stat)
        else:
            winners = event.resolve(star_selections)

        print("\n🏆 Contest Results:")
        print(f"Winners:")
        for winner in winners:
            print(f"{winner.name}")
            fan_card = self.fan_deck.draw()
            print(f"{winner.name} gains a {fan_card.name}!")
            winner.attached_fans.append(fan_card)

        self.discard_pile.append(event)

    def end_game(self):
        print("\n🏁 Game Over!")
        # TODO: Add Game Over logic, e.g. determine winner based on fans