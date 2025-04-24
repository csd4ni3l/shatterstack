import arcade, arcade.gui, random, math, json

from game.sprites import Shape
from utils.constants import SHAPES, CELL_SIZE, ROWS, COLS, menu_background_color, OUTLINE_WIDTH, COLORS, button_style
from utils.preload import button_texture, button_hovered_texture, click_sound

class Game(arcade.gui.UIView):
    def __init__(self, pypresence_client):
        super().__init__()
        self.shape_list = arcade.SpriteList()
        self.mouse_shape_list = arcade.SpriteList()

        self.pypresence_client = pypresence_client

        self.occupied = {}
        self.shapes = []

        self.shape_to_place = random.choice(list(SHAPES.keys()))
        self.shape_color = random.choice(list(COLORS.values()))

        self.next_shape_to_place = random.choice(list(SHAPES.keys()))
        self.next_shape_color = random.choice(list(COLORS.values()))

        self.start_x = self.window.width / 2 - (COLS * (CELL_SIZE + OUTLINE_WIDTH)) / 2 + (CELL_SIZE / 2)
        self.start_y = self.window.height - (ROWS * (CELL_SIZE + OUTLINE_WIDTH)) - (CELL_SIZE / 2)

        self.score = 0

        self.anchor = self.add_widget(arcade.gui.UIAnchorLayout())

        with open("settings.json", "r") as file:
            self.settings_dict = json.load(file)

    def main_exit(self):
        self.window.set_mouse_visible(True)

        from menus.main import Main
        self.window.show_view(Main())

    def on_mouse_motion(self, x, y, dx, dy):
        super().on_mouse_motion(x, y, dx, dy)
        self.mouse_shape.update(self.shape_to_place, self.shape_color, x, y)

    def on_show_view(self):
        super().on_show_view()

        self.setup_grid()

        self.mouse_shape = Shape(0, 0, self.shape_to_place, self.shape_color, self.mouse_shape_list)
        self.next_shape_ui = Shape(self.window.width - (CELL_SIZE * 4), self.window.height - (CELL_SIZE * 4), self.next_shape_to_place, self.next_shape_color, self.shape_list)

        self.score_label = self.anchor.add(arcade.gui.UILabel(text="Score: 0", font_name="Protest Strike", font_size=24), anchor_x="center", anchor_y="top")

        self.back_button = arcade.gui.UITextureButton(texture=button_texture, texture_hovered=button_hovered_texture, text='<--', style=button_style, width=100, height=50)
        self.back_button.on_click = lambda e: self.main_exit()
        self.anchor.add(self.back_button, anchor_x="left", anchor_y="top", align_x=5, align_y=-5)

        self.pypresence_client.update(state='In Game', details='Shattering Stacks', start=self.pypresence_client.start_time)

        self.window.set_mouse_visible(False)

    def setup_grid(self):
        for row in range(ROWS):
            self.occupied[row] = {}
            for col in range(COLS):
                self.occupied[row][col] = 0
                center_x = self.start_x + col * (CELL_SIZE + OUTLINE_WIDTH)
                center_y = self.start_y + row * (CELL_SIZE + OUTLINE_WIDTH)

                self.shape_list.append(arcade.SpriteSolidColor(
                    width=CELL_SIZE,
                    height=CELL_SIZE,
                    color=arcade.color.GRAY,
                    center_x=center_x,
                    center_y=center_y
                ))

    def check_occupation(self, grid_col, grid_row):
        can_place = True

        center_x, center_y = 0, 0

        if 0 <= grid_row < ROWS and 0 <= grid_col < COLS:
            for offset_col, offset_row in SHAPES[self.shape_to_place]:
                tile_col = grid_col + offset_col
                tile_row = grid_row + offset_row

                if not (0 <= tile_row < ROWS and 0 <= tile_col < COLS) or self.occupied[tile_row][tile_col]:
                    can_place = False
                    break

                center_x = self.start_x + grid_col * (CELL_SIZE + OUTLINE_WIDTH)
                center_y = self.start_y + grid_row * (CELL_SIZE + OUTLINE_WIDTH)
        else:
            can_place = False

        return can_place, center_x, center_y

    def check_collisions(self):
        for row_idx, row in self.occupied.items():
            if all(row.values()):
                for tile in row.values():
                    self.shape_list.remove(tile)

                for col in range(COLS):
                    self.occupied[row_idx][col] = 0
                    self.score += 25

        for col in range(COLS):
            column = [row[col] for row in self.occupied.values()]
            if all(column):
                for tile in column:
                    self.shape_list.remove(tile)

                for row_idx in range(ROWS):
                    self.occupied[row_idx][col] = 0
                    self.score += 25

    def update_game(self):
        self.check_collisions()
        self.score_label.text = f"Score: {self.score}"
        self.check_game_over()

    def check_game_over(self):
        for grid_row in range(ROWS):
            for grid_col in range(COLS):
                can_place, *_ = self.check_occupation(grid_col, grid_row)
                if can_place:
                    return

        self.game_over_label = self.anchor.add(arcade.gui.UILabel(text="GAME OVER", font_name="Protest Strike", font_size=64), anchor_x="center", anchor_y="center")

        self.shape_list.clear()
        self.mouse_shape_list.clear()

        self.window.set_mouse_visible(True)

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        super().on_key_press(symbol, modifiers)
        if symbol == arcade.key.ESCAPE:
            self.main_exit()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> bool | None:
        super().on_mouse_press(x, y, button, modifiers)

        if self.settings_dict.get("sfx", True):
            click_sound.play(volume=self.settings_dict.get("sfx_volume", 50) / 100)

        grid_col = math.ceil((x - self.start_x + (CELL_SIZE / 2)) // (CELL_SIZE + OUTLINE_WIDTH))
        grid_row = math.ceil((y - self.start_y + (CELL_SIZE / 2)) // (CELL_SIZE + OUTLINE_WIDTH))

        can_place, center_x, center_y = self.check_occupation(grid_col, grid_row)

        if can_place:
            shape = Shape(center_x, center_y, self.shape_to_place, self.shape_color, self.shape_list)
            self.shapes.append(shape)

            n = 0

            for offset_col, offset_row in SHAPES[self.shape_to_place]:
                tile_col = grid_col + offset_col
                tile_row = grid_row + offset_row
                self.occupied[tile_row][tile_col] = shape.tiles[n]

                n += 1

                self.score += 5

            self.shape_to_place = self.next_shape_to_place
            self.shape_color = self.next_shape_color

            self.update_game()

            self.next_shape_to_place = random.choice(list(SHAPES.keys()))
            self.next_shape_color = random.choice(list(COLORS.values()))
            self.next_shape_ui.update(self.next_shape_to_place, self.next_shape_color)

    def on_draw(self):
        super().on_draw()
        self.shape_list.draw()
        self.mouse_shape_list.draw()
