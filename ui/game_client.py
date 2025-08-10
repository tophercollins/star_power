import dearpygui.dearpygui as dpg
import logging

logger = logging.getLogger(__name__)

class GameClient:
    def __init__(self, game):
        logger.info("Initializing GameClient")
        self.game = game
        dpg.create_context()
        dpg.create_viewport(title="Star Power", width=1025, height=900)
        self.setup_ui()
        self.state = self.game.snapshot()
        dpg.setup_dearpygui()
        self.refresh_zones()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

    def setup_ui(self):
        with dpg.window(label="Star Power", tag="root", width=1000, height=900, no_resize=True, no_move=True):
            # Top row: Deck (left) + Board (right)
            with dpg.group(horizontal=True):
                with dpg.child_window(tag="deck_zone", width=200, height=580, border=True):
                    pass
                with dpg.child_window(tag="board_zone", width=-1, height=580, border=True):
                    pass
            # Bottom row: Hand
            with dpg.child_window(tag="hand_zone", height=230, border=True):
                pass

    
    def refresh_zones(self):
        self.state = self.game.snapshot()

        # Clear zones
        for zone in ("deck_zone", "hand_zone", "board_zone"):
            for child in dpg.get_item_children(zone, 1) or []:
                dpg.delete_item(child)


        # Player State
        players = self.state["players"]
        user_view = self.state["players"][0]
        opponent_view = self.state["players"][1]
        

        # Deck
        main_deck_view = self.state.get("main_deck")
        event_deck_view = self.state.get("event_deck")
        fan_deck_view = self.state.get("fan_deck")
        if main_deck_view:
            dpg.add_text(
                f"{main_deck_view.get('name','Main Deck')} ({main_deck_view.get('size') or main_deck_view.get('count', 0)} cards)",
                parent="deck_zone"
            )
        if event_deck_view:
            dpg.add_text(
                f"{event_deck_view.get('name','Event Deck')} ({event_deck_view.get('size') or event_deck_view.get('count', 0)} cards)",
                parent="deck_zone"
            )
        if fan_deck_view:
            dpg.add_text(
                f"{fan_deck_view.get('name','Fan Deck')} ({fan_deck_view.get('size') or fan_deck_view.get('count', 0)} cards)",
                parent="deck_zone"
            )
        if not any([main_deck_view, event_deck_view, fan_deck_view]):
            dpg.add_text("Decks unavailable", parent="deck_zone")


        # Board
        dpg.add_text("Board:", parent="board_zone")
        
        dpg.add_text(f"{opponent_view.get('name','Opponent')}'s Stars:", parent="board_zone")
        opp_board_row = dpg.add_group(horizontal=True, parent="board_zone")
        
        for star_view in (opponent_view.get("stars", []) or []):
            self.display_star_card(star_view, parent=opp_board_row)

        dpg.add_spacer(height=10, parent="board_zone")
        dpg.add_text(f"{user_view.get('name','You')}'s Stars:", parent="board_zone")

        user_board_row = dpg.add_group(horizontal=True, parent="board_zone")
        
        for star_view in (user_view.get("stars", []) or []):
            self.display_star_card(star_view, parent=user_board_row)


        # Hand
        user_name = user_view.get("name", "Player")
        dpg.add_text(f"{user_name}'s Hand:", parent="hand_zone")
        hand_row = dpg.add_group(horizontal=True, parent="hand_zone", tag="hand_row")
        user_hand_cards = user_view.get("hand", []) or []
        if user_hand_cards:
            for card_view in user_hand_cards:
                self.display_star_card(card_view, parent=hand_row)
        else:
            dpg.add_text("(empty)", parent=hand_row)


    def on_card_action(self, command: dict) -> None:
        self.game.dispatch(command)
        self.refresh_zones()

    def _card_button_callback(self, sender, app_data, user_data):
        self.on_card_action(user_data)

    def display_star_card(
            self, 
            card_view, 
            parent):
        with dpg.child_window(parent=parent, width=120, height=180, border=True):
            dpg.add_text(card_view.get("name", "Star"))
            dpg.add_spacer(height=5)
            dpg.add_text(f"Aura: {card_view.get('aura', 0)}")
            dpg.add_text(f"Influence: {card_view.get('influence', 0)}")
            dpg.add_text(f"Talent: {card_view.get('talent', 0)}")
            dpg.add_text(f"Legacy: {card_view.get('legacy', 0)}")

            if card_view.get("show_button", False):
                dpg.add_spacer(height=10)
                dpg.add_button(
                    label=card_view.get("button_label", "Play"),
                    enabled=True,
                    callback=self._card_button_callback,
                    user_data=card_view.get("button_command", "Play"),
                )