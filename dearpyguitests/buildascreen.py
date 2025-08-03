import dearpygui.dearpygui as dpg
from random import shuffle

# DUMMY DECK

DECK = [{"name": f"Card {i}"} for i in range(1, 11)]
HAND = []
BOARD = []
shuffle(DECK)

# REFRESH SCREEN
def refresh_zones():
    # clear zones (remove children)
    for zone in ("opponent_hand_zone", "deck_zone", "hand_zone", "board_zone"):
        for child in dpg.get_item_children(zone, 1) or []:
            dpg.delete_item(child)
    # repopulate zone titles
    dpg.add_text("Opponent's Hand", parent="opponent_hand_zone")
    dpg.add_text("Decks", parent="deck_zone")
    dpg.add_text("Board", parent="board_zone")
    dpg.add_text("Your Hand", parent="hand_zone")
    # repopulate deck
    for card in DECK:
        dpg.add_button(label=card["name"],
                       parent="deck_zone",
                       callback=move_card, 
                       user_data=("DECK", card))
    # repopulate board
    for card in BOARD:
        dpg.add_button(label=card["name"], 
                       parent="board_zone") 
    # repopulate hand
    for card in HAND:
        dpg.add_button(label=card["name"],
                        parent="hand_zone",
                        callback=move_card, 
                        user_data=("HAND_TO_BOARD", card))
        
# MOVE CARD
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
dpg.create_viewport(title="Star Power", width=1000, height=950)

with dpg.window(label="Card Game", width=-1, height=-1):
    with dpg.group(horizontal=False):
        with dpg.child_window(tag="opponent_hand_zone", width=960, height=200, border=True): pass
        with dpg.group(horizontal=True):
            with dpg.child_window(tag="deck_zone", width=200, height=420, border=True): pass
            with dpg.child_window(tag="board_zone", width=-1, height=420, border=True): pass
        with dpg.child_window(tag="hand_zone", width=960, height=200, border=True): pass

dpg.setup_dearpygui()
refresh_zones()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()