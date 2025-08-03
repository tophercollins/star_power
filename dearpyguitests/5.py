import dearpygui.dearpygui as dpg

def on_drop(sender, app_data, user_data):
    dpg.set_value("status", f"Dropped: {app_data}")

dpg.create_context()
dpg.create_viewport(title="DPG 1.11.1 DragDrop", width=400, height=200)

with dpg.window(label="Demo", width=380, height=160):
    src = dpg.add_button(label="Drag me")
    with dpg.drag_payload(parent=src, payload_type="X", drag_data=("HELLO", 123)):
        dpg.add_text("Dragging…")

    dst = dpg.add_button(label="Drop here")
    with dpg.drop_target(parent=dst, payload_type="X"):
        dpg.add_text("Target ready")
        dpg.add_drag_payload_callback(callback=on_drop)

    dpg.add_text("", tag="status")

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
