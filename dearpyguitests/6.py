# step_6_theme_font.py
import dearpygui.dearpygui as dpg

dpg.create_context()
with dpg.font_registry():
    default_font = dpg.add_font(dpg.get_system_font_name(), 18)

with dpg.theme() as card_theme:
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (80, 80, 80))
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 8)

dpg.create_viewport(title="Style Sample", width=500, height=300)

with dpg.window(label="Style"):
    dpg.add_button(label="Card", tag="card_btn")
    dpg.bind_item_theme("card_btn", card_theme)
    dpg.add_spacer(height=8)
    dpg.add_text("Fonts applied")

dpg.bind_font(default_font)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
