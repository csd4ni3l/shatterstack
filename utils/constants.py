import arcade.color
from arcade.types import Color
from arcade.gui.widgets.buttons import UITextureButtonStyle

menu_background_color = Color(28, 28, 28)
log_dir = 'logs'
CELL_SIZE = 48
ROWS = 14
COLS = 14
OUTLINE_WIDTH = 2

button_style = {'normal': UITextureButtonStyle(font_name="Protest Strike", font_color=arcade.color.BLACK), 'hover': UITextureButtonStyle(font_name="Protest Strike", font_color=arcade.color.BLACK),
                'press': UITextureButtonStyle(font_name="Protest Strike", font_color=arcade.color.BLACK), 'disabled': UITextureButtonStyle(font_name="Protest Strike", font_color=arcade.color.BLACK)}

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
    "S":      [(1, 0), (2, 0), (0, 1), (1, 1)],
    "S_R1":   [(0, 0), (0, 1), (1, 1), (1, 2)],
    "Z":      [(0, 0), (1, 0), (1, 1), (2, 1)],
    "Z_R1":   [(1, 0), (0, 1), (1, 1), (0, 2)],
    "BLOB": [
        (0, 0), (1, 0), (2, 0),
        (0, 1), (1, 1), (2, 1),
        (0, 2), (1, 2), (2, 2)
    ],
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
