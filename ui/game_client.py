import dearpygui.dearpygui as dpg

class GameClient:
    def __init__(self, game):
        self.game = game
        self.player = game.players[0]  # only show first human player
        dpg.create_context()
        dpg.create_viewport(title="Star Power - Game Client", width=1000, height=600)
        self.setup_ui()
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

    def setup_ui(self):
        with dpg.window(label="Player 1 Hand", width=-1, height=-1):
            dpg.add_text(f"{self.player.name}'s Hand")

            with dpg.group(horizontal=True):
                for card in self.player.hand:
                    if hasattr(card, 'aura'):  # crude check for StarCard (can be improved)
                        self.display_star_card(card)

    def display_star_card(self, card):
        with dpg.child_window(width=120, height=160, border=True):
            dpg.add_text(card.name)
            dpg.add_spacer(height=5)
            dpg.add_text(f"Aura: {card.aura}")
            dpg.add_text(f"Influence: {card.influence}")
            dpg.add_text(f"Talent: {card.talent}")
            dpg.add_text(f"Legacy: {card.legacy}")
