import dearpygui.dearpygui as dpg
from random import shuffle

# DUMMY DECK

DECK = [{"name": f"Card {i}"} for i in range(1, 11)]
HAND = []
BOARD = []
shuffle(DECK)

# CARD DISPLAY

def view_card(card, parent, callback=None, user_data=None):

    with dpg.child_window(parent=parent, width=120, height=170, border=True) as card_container:

        # Card name at the top
        dpg.add_text(card["name"])
        dpg.add_spacer(height=2)

        # Stats section
        with dpg.group(horizontal=False):
            dpg.add_text(f"Aura: {card.get('aura', 0)}")
            dpg.add_text(f"Influence: {card.get('influence', 0)}")
            dpg.add_text(f"Talent: {card.get('talent', 0)}")
            dpg.add_text(f"Legacy: {card.get('legacy', 0)}")

        dpg.add_spacer(height=2)

        # Click button (optional)
        if callback:
            dpg.add_button(label="Play", width=-1, height=24, callback=callback, user_data=user_data)

# REFRESH SCREEN
def refresh_zones():
    # clear zones (remove children)
    for zone in ("deck_zone", "hand_zone", "board_zone"):
        for child in dpg.get_item_children(zone, 1) or []:
            dpg.delete_item(child)
    # repopulate zone titles
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
    with dpg.group(horizontal=True, parent="board_zone") as board_group:
        for card in BOARD:
            view_card(card=card,
                      parent=board_group)

    # repopulate hand
    with dpg.group(horizontal=True, parent="hand_zone") as hand_group:
        for card in HAND:
            view_card(card=card,
                      parent=hand_group,
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
dpg.create_viewport(title="Star Power", width=1000, height=1050)

with dpg.window(label="Card Game", width=-1, height=-1):
    with dpg.group(horizontal=False):
        with dpg.group(horizontal=True):
            with dpg.child_window(tag="deck_zone", width=200, height=460, border=True): pass
            with dpg.child_window(tag="board_zone", width=-1, height=460, border=True): pass
        with dpg.child_window(tag="hand_zone", width=960, height=220, border=True): pass

dpg.setup_dearpygui()
refresh_zones()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()