import arcade.gui, arcade

button_texture = arcade.gui.NinePatchTexture(64 // 4, 64 // 4, 64 // 4, 64 // 4, arcade.load_texture("assets/graphics/button.png"))
button_hovered_texture = arcade.gui.NinePatchTexture(64 // 4, 64 // 4, 64 // 4, 64 // 4, arcade.load_texture("assets/graphics/button_hovered.png"))

theme_sound = arcade.Sound("assets/sound/music.ogg")
click_sound = arcade.Sound("assets/sound/click.wav")
