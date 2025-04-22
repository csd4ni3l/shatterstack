import arcade, arcade.gui, asyncio, pypresence, time
from utils.preload import button_texture, button_hovered_texture
from utils.constants import button_style
from utils.utils import FakePyPresence

class Main(arcade.gui.UIView):
    def __init__(self, pypresence_client=None):
        super().__init__()

        self.anchor = self.add_widget(arcade.gui.UIAnchorLayout())
        self.box = self.anchor.add(arcade.gui.UIBoxLayout(space_between=10), anchor_x='center', anchor_y='center')

        self.pypresence_client = pypresence_client

        if self.pypresence_client == None: # Game has started
            try:
                asyncio.get_event_loop()
            except:
                asyncio.set_event_loop(asyncio.new_event_loop())
            try:
                self.pypresence_client = pypresence.Presence(1360953272843632680)
                self.pypresence_client.connect()
                self.pypresence_client.start_time = time.time()
            except:
                self.pypresence_client = FakePyPresence()
                self.pypresence_client.start_time = time.time()

        elif isinstance(self.pypresence_client, FakePyPresence):
            # get start time from old object
            start_time = copy.deepcopy(self.pypresence_client.start_time)
            try:
                self.pypresence_client = pypresence.Presence(1360953272843632680)
                self.pypresence_client.connect()
                self.pypresence_client.start_time = start_time
            except:
                self.pypresence_client = FakePyPresence()
                self.pypresence_client.start_time = start_time

        self.pypresence_client.update(state='In Menu', details='In Main Menu', start=self.pypresence_client.start_time)

    def on_show_view(self):
        super().on_show_view()

        self.title_label = self.box.add(arcade.gui.UILabel(text="ShatterStack", font_name="Protest Strike", font_size=48))

        self.play_button = self.box.add(arcade.gui.UITextureButton(text="Play", texture=button_texture, texture_hovered=button_hovered_texture, width=self.window.width / 2, height=150, style=button_style))
        self.play_button.on_click = lambda event: self.play()

        self.settings_button = self.box.add(arcade.gui.UITextureButton(text="Settings", texture=button_texture, texture_hovered=button_hovered_texture, width=self.window.width / 2, height=150, style=button_style))
        self.settings_button.on_click = lambda event: self.settings()

    def play(self):
        from game.play import Game
        self.window.show_view(Game(self.pypresence_client))

    def settings(self):
        from menus.settings import Settings
        self.window.show_view(Settings(self.pypresence_client))
