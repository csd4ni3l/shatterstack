import os, arcade, arcade.gui, random, json, time

from game.sprites import Shape
from utils.constants import SHAPES, CELL_SIZE, ROWS, COLS, OUTLINE_WIDTH, COLORS, COMBO_TIME, button_style
from utils.preload import button_texture, button_hovered_texture, click_sound, break_sound
class Game(arcade.gui.UIView):
    def __init__(self, pypresence_client):
        super().__init__()
        self.shape_list = arcade.SpriteList()
        self.mouse_shape_list = arcade.SpriteList()

        self.pypresence_client = pypresence_client

        self.occupied = {}
        self.shapes = []

        self.shape_to_place = random.choice(list(SHAPES.keys()))
        self.shape_color = random.choice(COLORS)

        self.next_shape_to_place = random.choice(list(SHAPES.keys()))
        self.next_shape_color = random.choice(COLORS)

        self.start_x = self.window.width / 2 - (COLS * (CELL_SIZE + OUTLINE_WIDTH)) / 2 + (CELL_SIZE / 2)
        self.start_y = self.window.height - (ROWS * (CELL_SIZE + OUTLINE_WIDTH)) - (CELL_SIZE / 2)
        self.shape_center_x = 0
        self.shape_center_y = 0
        self.can_place_shape = True
        self.empty_grid = {}

        if os.path.exists("data.json"):
            with open("data.json", "r") as file:
                self.high_score = json.load(file)["high_score"]
        else:
            self.high_score = 0

        self.score = 0
        self.combo = 0
        self.last_combo = time.perf_counter()

        self.anchor = self.add_widget(arcade.gui.UIAnchorLayout())

        with open("settings.json", "r") as file:
            self.settings_dict = json.load(file)

    def main_exit(self):
        self.window.set_mouse_visible(True)

        with open("data.json", "w") as file:
            file.write(json.dumps({"high_score": self.high_score}))

        from menus.main import Main
        self.window.show_view(Main())

    def on_show_view(self):
        super().on_show_view()

        self.setup_grid()

        self.mouse_shape = Shape(0, 0, self.shape_to_place, self.shape_color, self.mouse_shape_list)
        self.next_shape_ui = Shape(self.window.width - (CELL_SIZE * 3), self.window.height - (CELL_SIZE * 3), self.next_shape_to_place, self.next_shape_color, self.shape_list)

        self.score_box = self.anchor.add(arcade.gui.UIBoxLayout(space_between=10, vertical=False), anchor_x="center", anchor_y="top")

        self.score_label = self.score_box.add(arcade.gui.UILabel(text="Score: 0", font_name="Roboto", font_size=24))
        self.high_score_label = self.score_box.add(arcade.gui.UILabel(text=f"High Score: {self.high_score}", font_name="Roboto", font_size=24))

        self.back_button = arcade.gui.UITextureButton(texture=button_texture, texture_hovered=button_hovered_texture, text='<--', style=button_style, width=100, height=50)
        self.back_button.on_click = lambda e: self.main_exit()
        self.anchor.add(self.back_button, anchor_x="left", anchor_y="top", align_x=5, align_y=-5)
        
        self.combo_label = self.anchor.add(arcade.gui.UILabel(text=f"Combo X{self.combo}", font_name="Roboto", font_size=32), anchor_x="center", anchor_y="center")
        self.combo_label.visible = False
        
        self.pypresence_client.update(state='In Game', details='Shattering Stacks', start=self.pypresence_client.start_time)

        self.window.set_mouse_visible(False)

    def on_stick_motion(self, controller, name, value):
        if name == "leftstick":
            value *= 10
            self.on_mouse_motion(self.mouse_shape.x + value.x, self.mouse_shape.y + value.y, value.x, value.y)

    def on_button_press(self, controller, name):
        if name == "a":
            self.on_mouse_press(self.mouse_shape.x, self.mouse_shape.y, arcade.MOUSE_BUTTON_LEFT, 0)
        elif name == "start":
            self.main_exit()

    def on_mouse_motion(self, x, y, dx, dy):
        grid_col = int((x - self.start_x + (CELL_SIZE / 2)) // (CELL_SIZE + OUTLINE_WIDTH))
        grid_row = int((y - self.start_y + (CELL_SIZE / 2)) // (CELL_SIZE + OUTLINE_WIDTH))

        self.can_place_shape = True
        tile_positions = []
        for offset_col, offset_row in SHAPES[self.shape_to_place]:
            tile_col = grid_col + offset_col
            tile_row = grid_row + offset_row

            if not (0 <= tile_row < ROWS and 0 <= tile_col < COLS) or self.occupied[tile_row][tile_col]:
                self.can_place_shape = False
                break

            tile_positions.append((tile_row, tile_col))

            self.shape_center_x = self.start_x + grid_col * (CELL_SIZE + OUTLINE_WIDTH)
            self.shape_center_y = self.start_y + grid_row * (CELL_SIZE + OUTLINE_WIDTH)

        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_grid[row][col]:
                    self.empty_grid[row][col].color = (*self.shape_color[:-1], 170) if self.can_place_shape and (row, col) in tile_positions else arcade.color.GRAY

        self.mouse_shape.update(self.shape_to_place, self.shape_color, x, y)

    def setup_grid(self):
        for row in range(ROWS):
            self.occupied[row] = {}
            self.empty_grid[row] = {}

            for col in range(COLS):
                self.occupied[row][col] = 0

                center_x = self.start_x + col * (CELL_SIZE + OUTLINE_WIDTH)
                center_y = self.start_y + row * (CELL_SIZE + OUTLINE_WIDTH)
                tile = arcade.SpriteSolidColor(
                    width=CELL_SIZE,
                    height=CELL_SIZE,
                    color=arcade.color.GRAY,
                    center_x=center_x,
                    center_y=center_y
                )
                self.shape_list.append(tile)

                self.empty_grid[row][col] = tile

    def check_collisions(self):
        for row_idx, row in self.occupied.items():
            if all(row.values()):
                for tile in row.values():
                    self.shape_list.remove(tile)

                for col in range(COLS):
                    self.occupied[row_idx][col] = 0
                    center_x = self.start_x + col * (CELL_SIZE + OUTLINE_WIDTH)
                    center_y = self.start_y + row_idx * (CELL_SIZE + OUTLINE_WIDTH)
                    tile = arcade.SpriteSolidColor(
                        width=CELL_SIZE,
                        height=CELL_SIZE,
                        color=arcade.color.GRAY,
                        center_x=center_x,
                        center_y=center_y
                    )
                    self.shape_list.append(tile)
                    self.empty_grid[row_idx][col] = tile

                    self.score += 25 + (10 * self.combo)
            
                break_sound.play()

                self.combo += 1
                self.last_combo = time.perf_counter()

        for col in range(COLS):
            column = [row[col] for row in self.occupied.values()]
            if all(column):
                for tile in column:
                    self.shape_list.remove(tile)

                for row_idx in range(ROWS):
                    self.occupied[row_idx][col] = 0
                    center_x = self.start_x + col * (CELL_SIZE + OUTLINE_WIDTH)
                    center_y = self.start_y + row_idx * (CELL_SIZE + OUTLINE_WIDTH)
                    tile = arcade.SpriteSolidColor(
                        width=CELL_SIZE,
                        height=CELL_SIZE,
                        color=arcade.color.GRAY,
                        center_x=center_x,
                        center_y=center_y
                    )
                    self.shape_list.append(tile)
                    self.empty_grid[row_idx][col] = tile
                    
                    self.score += 25 + (10 * self.combo)

                break_sound.play()
                self.combo += 1
                self.last_combo = time.perf_counter()

    def update_game(self):
        self.check_collisions()
        
        self.score_label.text = f"Score: {self.score}" + (f" Combo: X{self.combo}" if self.combo else "")
        
        if self.score > self.high_score:
            self.high_score = self.score
            self.high_score_label.text = f"High Score: {self.high_score}"

        if time.perf_counter() - self.last_combo >= COMBO_TIME:
            self.combo = 0

        self.check_game_over()

    def check_game_over(self):
        for grid_row in range(ROWS):
            for grid_col in range(COLS):
                can_place = True
                
                for offset_col, offset_row in SHAPES[self.shape_to_place]:
                    tile_col = grid_col + offset_col
                    tile_row = grid_row + offset_row

                    if not (0 <= tile_row < ROWS and 0 <= tile_col < COLS) or self.occupied[tile_row][tile_col]:
                        can_place = False

                if can_place:
                    return

        self.game_over_label = self.anchor.add(arcade.gui.UILabel(text="GAME OVER", font_name="Roboto", font_size=64), anchor_x="center", anchor_y="center")

        self.shape_list.clear()
        self.mouse_shape_list.clear()
        self.anchor.remove(self.combo_label)

        self.window.set_mouse_visible(True)

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        super().on_key_press(symbol, modifiers)
        if symbol == arcade.key.ESCAPE:
            self.main_exit()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> bool | None:
        super().on_mouse_press(x, y, button, modifiers)

        grid_col = int((x - self.start_x + (CELL_SIZE / 2)) // (CELL_SIZE + OUTLINE_WIDTH))
        grid_row = int((y - self.start_y + (CELL_SIZE / 2)) // (CELL_SIZE + OUTLINE_WIDTH))

        if self.can_place_shape:
            if self.settings_dict.get("sfx", True):
                click_sound.play(volume=self.settings_dict.get("sfx_volume", 50) / 100)
    
            shape = Shape(self.shape_center_x, self.shape_center_y, self.shape_to_place, self.shape_color, self.shape_list)
            self.shapes.append(shape)

            n = 0

            for offset_col, offset_row in SHAPES[self.shape_to_place]:
                tile_col = grid_col + offset_col
                tile_row = grid_row + offset_row
                self.occupied[tile_row][tile_col] = shape.tiles[n]
                self.shape_list.remove(self.empty_grid[tile_row][tile_col])
                self.empty_grid[tile_row][tile_col] = None

                n += 1

                self.score += 5

            self.shape_to_place = self.next_shape_to_place
            self.shape_color = self.next_shape_color

            self.update_game()

            self.next_shape_to_place = random.choice(list(SHAPES.keys()))
            self.next_shape_color = random.choice(COLORS)
            self.next_shape_ui.update(self.next_shape_to_place, self.next_shape_color)

    def on_draw(self):
        self.window.clear()
        self.shape_list.draw()
        self.mouse_shape_list.draw()
        self.ui.draw()