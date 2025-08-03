"""
Base screen scaffold for a card game UI using Dear PyGui.
- Viewport 1280x720 with docking enabled
- Named regions: Board, Player Hand, Opponent Area, Side Panel, Log
- Top menu bar with File/View/Help
- Status bar along the bottom
- Theme + font loading
- Resize-aware layout using handlers

Run:  python main.py
Requires: dearpygui>=1.11
"""

import sys
from pathlib import Path

try:
    import dearpygui.dearpygui as dpg
except Exception as e:
    print("Dear PyGui is required. Install with: pip install dearpygui", file=sys.stderr)
    raise

APP_TITLE = "Card Game – Base Screen"
VIEWPORT_W, VIEWPORT_H = 1280, 720

# --- Layout constants ---
SIDE_PANEL_MIN_W = 260
SIDE_PANEL_PREF_W = 320
LOG_PANEL_MIN_H = 140
STATUS_BAR_H = 28


# --- Helper: compute dynamic sizes based on current viewport ---
def compute_layout_sizes():
    vp_w = dpg.get_viewport_width()
    vp_h = dpg.get_viewport_height()

    side_w = max(SIDE_PANEL_MIN_W, min(SIDE_PANEL_PREF_W, int(vp_w * 0.25)))
    content_w = max(320, vp_w - side_w)

    # remaining height after menu bar and status bar
    menu_h = dpg.get_item_height("menu_bar") if dpg.does_item_exist("menu_bar") else 28
    content_h = max(240, vp_h - menu_h - STATUS_BAR_H)

    # log area ~20% of vertical content, constrained
    log_h = max(LOG_PANEL_MIN_H, min(int(content_h * 0.25), 260))
    board_h = content_h - log_h

    return {
        "content_w": content_w,
        "side_w": side_w,
        "content_h": content_h,
        "log_h": log_h,
        "board_h": board_h,
    }


# --- Handlers ---
def refresh_layout():
    s = compute_layout_sizes()

    # Position/size main content (left)
    dpg.configure_item("content_region", width=s["content_w"], height=s["content_h"])
    dpg.configure_item("board_region", width=s["content_w"], height=s["board_h"])
    dpg.configure_item("log_region", width=s["content_w"], height=s["log_h"])

    # Side panel (right)
    dpg.configure_item("side_panel", width=s["side_w"], height=s["content_h"])

    # Sub-regions inside board
    # Opponent area: 30% height of board, Player area: 30%, Middle field: 40%
    opp_h = int(s["board_h"] * 0.3)
    mid_h = int(s["board_h"] * 0.4)
    ply_h = s["board_h"] - opp_h - mid_h

    dpg.configure_item("opponent_area", width=-1, height=opp_h)
    dpg.configure_item("field_area", width=-1, height=mid_h)
    dpg.configure_item("player_area", width=-1, height=ply_h)


def on_viewport_resize(sender, app_data):  # app_data: (width, height)
    refresh_layout()


# --- UI builders ---
def build_menu_bar():
    with dpg.viewport_menu_bar(tag="menu_bar"):
        with dpg.menu(label="File"):
            dpg.add_menu_item(label="New", callback=lambda: None)
            dpg.add_menu_item(label="Open…", callback=lambda: None)
            dpg.add_menu_item(label="Save Layout", callback=lambda: None)
            dpg.add_separator()
            dpg.add_menu_item(label="Exit", callback=lambda: dpg.stop_dearpygui())
        with dpg.menu(label="View"):
            dpg.add_menu_item(label="Toggle Side Panel", callback=lambda: dpg.configure_item("side_panel", show=not dpg.is_item_shown("side_panel")))
            dpg.add_menu_item(label="Toggle Log", callback=lambda: dpg.configure_item("log_region", show=not dpg.is_item_shown("log_region")))
        with dpg.menu(label="Help"):
            dpg.add_menu_item(label="About", callback=lambda: dpg.show_item("about_modal"))


def build_status_bar():
    with dpg.window(tag="status_bar", no_title_bar=True, no_move=True, no_resize=True, no_scrollbar=True, no_collapse=True, horizontal_scrollbar=False, pos=(0, VIEWPORT_H-STATUS_BAR_H), height=STATUS_BAR_H):
        with dpg.group(horizontal=True):
            dpg.add_text("Ready", tag="status_text")
            dpg.add_spacer(width=10)
            dpg.add_separator()
            dpg.add_spacer(width=10)
            dpg.add_text("FPS:")
            dpg.add_text("0", tag="fps_text")


def build_about_modal():
    with dpg.window(label="About", modal=True, show=False, tag="about_modal", no_move=True, autosize=True):
        dpg.add_text("Card Game UI – Base Screen (Dear PyGui)")
        dpg.add_text("Use this scaffold as a starting point for your game UI.")
        dpg.add_separator()
        dpg.add_text("Regions:")
        dpg.add_text("Opponent Area", bullet=True)
        dpg.add_text("Field Area", bullet=True)
        dpg.add_text("Player Area", bullet=True)
        dpg.add_text("Side Panel (Deck/Turn/Controls)", bullet=True)
        dpg.add_text("Log Panel")
        dpg.add_separator()
        dpg.add_button(label="Close", width=120, callback=lambda: dpg.hide_item("about_modal"))


def labeled_panel(label, tag, **kwargs):
    with dpg.child_window(tag=tag, **kwargs):
        dpg.add_text(label, bullet=False)
        dpg.add_separator()
        return tag


def build_layout():
    # Root workspace window fills viewport content area under menu bar
    with dpg.window(tag="workspace", no_title_bar=True, no_move=True, no_resize=True, no_collapse=True):
        with dpg.group(horizontal=True):
            # Left content: board + log stacked vertically
            with dpg.group(tag="content_region"):
                with dpg.child_window(tag="board_region", border=False):
                    labeled_panel("Opponent Area", tag="opponent_area", border=True)
                    labeled_panel("Field Area", tag="field_area", border=True)
                    labeled_panel("Player Area", tag="player_area", border=True)
                labeled_panel("Log", tag="log_region", border=True)

            # Right side panel
            with dpg.child_window(tag="side_panel", border=True):
                dpg.add_text("Side Panel")
                dpg.add_separator()
                dpg.add_text("Turn: 1", tag="turn_text")
                dpg.add_text("Phase: Draw", tag="phase_text")
                dpg.add_separator()
                dpg.add_button(label="End Turn", width=-1)
                dpg.add_spacer(height=8)
                dpg.add_button(label="Shuffle", width=-1)
                dpg.add_spacer(height=8)
                dpg.add_button(label="Settings", width=-1, callback=lambda: dpg.show_item("about_modal"))


def apply_theme():
    with dpg.theme() as theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 8)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6)
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 6)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 6)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 10, 10)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 8, 6)
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 8)
    dpg.bind_theme(theme)


# --- Main ---
def main():
    dpg.create_context()

    # Fonts (optional)
    with dpg.font_registry():
        default_font_path_candidates = [
            "C:/Windows/Fonts/seguiemj.ttf",
            "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
        for p in default_font_path_candidates:
            if Path(p).exists():
                with dpg.font(p, 16, tag="default_font"):
                    dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
                dpg.bind_font("default_font")
                break

    dpg.configure_app(docking=True, docking_space=True)
    dpg.create_viewport(title=APP_TITLE, width=VIEWPORT_W, height=VIEWPORT_H)
    dpg.setup_dearpygui()

    build_menu_bar()
    build_layout()
    build_status_bar()
    build_about_modal()
    apply_theme()

    # Handler for viewport resize to keep layout fresh
    dpg.set_viewport_resize_callback(on_viewport_resize)

    dpg.show_viewport()

    # Position workspace below the menu bar
    dpg.set_primary_window("workspace", True)
    refresh_layout()

    # Simple runtime update: FPS display
    def update_status():
        dpg.set_value("fps_text", f"{dpg.get_frame_rate():.0f}")

    with dpg.item_handler_registry(tag="frame_handler") as ih:
        pass

    # Use a timer via render loop
    while dpg.is_dearpygui_running():
        update_status()
        dpg.render_dearpygui_frame()

    dpg.destroy_context()


if __name__ == "__main__":
    main()
