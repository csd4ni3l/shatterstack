import arcade
from utils.constants import SHAPES, CELL_SIZE, OUTLINE_WIDTH

class Shape():
    def __init__(self, x, y, shape_type, shape_color, sprite_list: arcade.SpriteList):
        self.x = x
        self.y = y
        self.sprite_list = sprite_list
        self.shape_type = shape_type
        self.shape_color = shape_color
        self.tiles = []

        self.setup_grid()

    def update(self, shape, color, x=None, y=None):
        if x:
            self.x = x
        if y:
            self.y = y

        self.shape_type = shape
        self.shape_color = color

        n = 0

        for tile in self.tiles:
            tile.visible = False

        for offset_col, offset_row in SHAPES[self.shape_type]:
            x = self.x + (offset_col * (CELL_SIZE + OUTLINE_WIDTH))
            y = self.y + (offset_row * (CELL_SIZE + OUTLINE_WIDTH))

            if n < len(self.tiles):
                self.tiles[n].position = x, y, 0
                self.tiles[n].color = color
                self.tiles[n].visible = True
            else:
                self.tiles.append(arcade.SpriteSolidColor(width=CELL_SIZE, height=CELL_SIZE,
                                                         color=color, center_x=x, center_y=y))
                self.sprite_list.append(self.tiles[-1])

            n += 1

    def setup_grid(self):
        for offset_col, offset_row in SHAPES[self.shape_type]:
            x = self.x + (offset_col * (CELL_SIZE + OUTLINE_WIDTH))
            y = self.y + (offset_row * (CELL_SIZE + OUTLINE_WIDTH))
            self.tiles.append(arcade.SpriteSolidColor(width=CELL_SIZE, height=CELL_SIZE,
                                                    color=self.shape_color, center_x=x, center_y=y))
            self.sprite_list.append(self.tiles[-1])
