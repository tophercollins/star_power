# step_3_layout.py
import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title="Card Game - Step 3", width=1000, height=700)

with dpg.window(label="Card Game", width=1000, height=700):
    with dpg.group(horizontal=True):
        with dpg.child_window(tag="deck_zone", width=200, height=600, border=True):
            dpg.add_text("Deck")
        with dpg.child_window(tag="board_zone", width=-1, height=600, border=True):
            dpg.add_text("Board")
    with dpg.child_window(tag="hand_zone", height=100, border=True):
        dpg.add_text("Hand")

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
