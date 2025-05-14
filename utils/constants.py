import arcade.color
from arcade.types import Color
from arcade.gui.widgets.buttons import UITextureButtonStyle, UIFlatButtonStyle
from arcade.gui.widgets.slider import UISliderStyle

menu_background_color = (30, 30, 47)
log_dir = 'logs'
discord_presence_id = 1360953272843632680

CELL_SIZE = 48
ROWS = 14
COLS = 14
OUTLINE_WIDTH = 2
SHAPES = {
    "I":      [(0, 0), (1, 0), (2, 0), (3, 0)],
    "I_R1":   [(0, 0), (0, 1), (0, 2), (0, 3)],
    "O":      [(0, 0), (1, 0), (0, 1), (1, 1)],
    "T":      [(0, 0), (1, 0), (2, 0), (1, 1)],
    "T_R1":   [(1, 0), (1, 1), (1, 2), (0, 1)],
    "T_R2":   [(0, 1), (1, 1), (2, 1), (1, 0)],
    "T_R3":   [(0, 0), (0, 1), (0, 2), (1, 1)],
    "L":      [(0, 0), (0, 1), (0, 2), (1, 2)],
    "L_R1":   [(0, 1), (1, 1), (2, 1), (2, 0)],
    "L_R2":   [(1, 0), (1, 1), (1, 2), (0, 0)],
    "L_R3":   [(0, 0), (1, 0), (2, 0), (0, 1)],
    "J":      [(1, 0), (1, 1), (1, 2), (0, 2)],
    "J_R1":   [(0, 0), (0, 1), (1, 1), (2, 1)],
    "J_R2":   [(0, 0), (1, 0), (0, 1), (0, 2)],
    "J_R3":   [(0, 0), (1, 0), (2, 0), (2, 1)],
    "LINE1": [(0, 0)],
    "LINE2": [(0, 0), (1, 0)],
    "LINE3": [(0, 0), (1, 0), (2, 0)],
}

COLORS = {
    "red": (255, 90, 90, 255),
    "blue": (100, 180, 255, 255),
    "green": (100, 255, 160, 255),
    "yellow": (255, 230, 100, 255),
    "purple": (200, 100, 255, 255),
    "orange": (255, 160, 90, 255),
    "teal": (100, 255, 255, 255),
}

button_style = {'normal': UITextureButtonStyle(font_name="Protest Strike", font_color=arcade.color.BLACK), 'hover': UITextureButtonStyle(font_name="Protest Strike", font_color=arcade.color.BLACK),
                'press': UITextureButtonStyle(font_name="Protest Strike", font_color=arcade.color.BLACK), 'disabled': UITextureButtonStyle(font_name="Protest Strike", font_color=arcade.color.BLACK)}
dropdown_style = {'normal': UIFlatButtonStyle(font_name="Protest Strike", font_color=arcade.color.BLACK, bg=Color(128, 128, 128)), 'hover': UIFlatButtonStyle(font_name="Protest Strike", font_color=arcade.color.BLACK, bg=Color(49, 154, 54)),
                  'press': UIFlatButtonStyle(font_name="Protest Strike", font_color=arcade.color.BLACK, bg=Color(128, 128, 128)), 'disabled': UIFlatButtonStyle(font_name="Protest Strike", font_color=arcade.color.BLACK, bg=Color(128, 128, 128))}

slider_default_style = UISliderStyle(bg=Color(128, 128, 128), unfilled_track=Color(128, 128, 128), filled_track=Color(49, 154, 54))
slider_hover_style = UISliderStyle(bg=Color(49, 154, 54), unfilled_track=Color(128, 128, 128), filled_track=Color(49, 154, 54))

slider_style = {'normal': slider_default_style, 'hover': slider_hover_style, 'press': slider_hover_style, 'disabled': slider_default_style}

settings = {
    "Graphics": {
        "Window Mode": {"type": "option", "options": ["Windowed", "Fullscreen", "Borderless"], "config_key": "window_mode", "default": "Windowed"},
        "Resolution": {"type": "option", "options": ["1366x768", "1440x900", "1600x900", "1920x1080", "2560x1440", "3840x2160"], "config_key": "resolution"},
        "Anti-Aliasing": {"type": "option", "options": ["None", "2x MSAA", "4x MSAA", "8x MSAA", "16x MSAA"], "config_key": "anti_aliasing", "default": "4x MSAA"},
        "VSync": {"type": "bool", "config_key": "vsync", "default": True},
        "FPS Limit": {"type": "slider", "min": 0, "max": 480, "config_key": "fps_limit", "default": 60},
    },
    "Sound": {
        "Music": {"type": "bool", "config_key": "music", "default": True},
        "SFX": {"type": "bool", "config_key": "sfx", "default": True},
        "Music Volume": {"type": "slider", "min": 0, "max": 100, "config_key": "music_volume", "default": 50},
        "SFX Volume": {"type": "slider", "min": 0, "max": 100, "config_key": "sfx_volume", "default": 50},
    },
    "Miscellaneous": {
        "Discord RPC": {"type": "bool", "config_key": "discord_rpc", "default": True},
    },
    "Credits": {}
}

settings_start_category = "Graphics"
