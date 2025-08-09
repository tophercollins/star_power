# step_4_cards_basic.py
import dearpygui.dearpygui as dpg
from random import shuffle

# --- simple game state ---
DECK = [{"name": f"Card {i}"} for i in range(1, 11)]
HAND = []
BOARD = []
shuffle(DECK)

def refresh_zones():
    # clear zones (remove children)
    for zone in ("deck_zone", "hand_zone", "board_zone"):
        for child in dpg.get_item_children(zone, 1) or []:
            dpg.delete_item(child)
    # repopulate
    dpg.add_text(f"Deck ({len(DECK)})", parent="deck_zone")
    for card in DECK:
        dpg.add_button(label=card["name"], parent="deck_zone",
                       callback=move_card, user_data=("DECK", card))
    dpg.add_text("Board:", parent="board_zone")
    for card in BOARD:
        dpg.add_button(label=card["name"], parent="board_zone")
    dpg.add_text("Hand:", parent="hand_zone")
    for card in HAND:
        dpg.add_button(label=card["name"], parent="hand_zone",
                       callback=move_card, user_data=("HAND_TO_BOARD", card))

def move_card(sender, app_data, user_data):
    where, card = user_data
    if where == "DECK":
        DECK.remove(card)
        HAND.append(card)
    elif where == "HAND_TO_BOARD":
        HAND.remove(card)
        BOARD.append(card)
    refresh_zones()

dpg.create_context()
dpg.create_viewport(title="Star Power", width=1000, height=900)

with dpg.window(label="Card Game", width=1000, height=700):
    with dpg.group(horizontal=True):
        with dpg.child_window(tag="deck_zone", width=200, height=600, border=True): pass
        with dpg.child_window(tag="board_zone", width=-1, height=600, border=True): pass
    with dpg.child_window(tag="hand_zone", height=100, border=True): pass

with dpg.handler_registry():
    dpg.add_key_press_handler(key=dpg.mvKey_R, callback=lambda: refresh_zones())  # press R to refresh

dpg.setup_dearpygui()
refresh_zones()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
