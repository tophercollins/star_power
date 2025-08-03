import dearpygui.dearpygui as dpg
print("Dear PyGui version:", dpg.get_version())
print("Has drop_target? ", hasattr(dpg, "drop_target"))
print("Has drag_payload? ", hasattr(dpg, "drag_payload"))