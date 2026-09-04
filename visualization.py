import arcade

WINDOW_TITLE = "FLY_IN"

WINDOW_WITH, WINDOW_HEIGHT = arcade.get_display_size()
NEW_WITH = WINDOW_WITH - 200
NEW_HEIGHT = WINDOW_HEIGHT - 200

class Visualization(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.AMAZON
        # self.history = history
        # self.graph = graph

    def reset(self):
        pass
    
    def on_draw(self):
        self.clear()

    def on_update(self, delta_time):
        pass

if __name__ == "__main__":
    window = arcade.Window(WINDOW_WITH, WINDOW_HEIGHT, WINDOW_TITLE)
    visualization = Visualization()
    window.show_view(visualization)
    arcade.run()
