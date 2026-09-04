import arcade


SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_display_size()
SCREEN_TITLE = "Drone Zone Visualizer"


class DroneVisualizer(arcade.Window):

    def __init__(self, graph, history):
        super().__init__(
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            title=SCREEN_TITLE,
            fullscreen=True
        )

        arcade.set_background_color(arcade.color.AMAZON)

        self.graph = graph
        self.turns = history
        self.current_turn = 0
        self.coordinate_scale = 200

        self.zone_position = {
            name: (
                zone.get_coordinates()[0] * self.coordinate_scale,
                zone.get_coordinates()[1] * self.coordinate_scale
            )
            for name, zone in graph.zones.items()
        }

        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()

        self.camera_move_speed = 1000
        self.keys_held = set()

        self.turn_change_delay = 0.15
        self.turn_change_timer = 0

        self.dragging = False

        self.center_camera_on_graph()

    def center_camera_on_graph(self):
        if not self.zone_position:
            return

        xs = [position[0] for position in self.zone_position.values()]
        ys = [position[1] for position in self.zone_position.values()]

        min_x = min(xs)
        max_x = max(xs)
        min_y = min(ys)
        max_y = max(ys)

        self.camera.position = (
            (min_x + max_x) / 2,
            (min_y + max_y) / 2
        )

        graph_width = max(max_x - min_x, 1) + 300
        graph_height = max(max_y - min_y, 1) + 300

        zoom = min(
            SCREEN_WIDTH / graph_width,
            SCREEN_HEIGHT / graph_height
        )

        self.camera.zoom = max(0.1, min(zoom, 2.0))

    def reset_camera(self):
        self.center_camera_on_graph()

    def on_key_press(self, key, modifiers):
        self.keys_held.add(key)

        if key == arcade.key.R:
            self.reset_camera()

    def on_key_release(self, key, modifiers):
        self.keys_held.discard(key)

    def on_update(self, delta_time):
        move_x = 0
        move_y = 0

        if arcade.key.W in self.keys_held:
            move_y += 1

        if arcade.key.S in self.keys_held:
            move_y -= 1

        if arcade.key.A in self.keys_held:
            move_x -= 1

        if arcade.key.D in self.keys_held:
            move_x += 1

        if move_x and move_y:
            move_x *= 0.7071
            move_y *= 0.7071

        if move_x or move_y:
            self.camera.position = (
                self.camera.position[0] + move_x * self.camera_move_speed * delta_time,
                self.camera.position[1] + move_y * self.camera_move_speed * delta_time
            )

        self.turn_change_timer += delta_time

        if self.turn_change_timer >= self.turn_change_delay:
            if arcade.key.UP in self.keys_held:
                if self.current_turn < len(self.turns) - 1:
                    self.current_turn += 1
                self.turn_change_timer = 0

            elif arcade.key.DOWN in self.keys_held:
                if self.current_turn > 0:
                    self.current_turn -= 1
                self.turn_change_timer = 0

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        scroll = scroll_y or scroll_x

        if scroll > 0:
            self.camera.zoom *= 1.15

        elif scroll < 0:
            self.camera.zoom /= 1.15

        self.camera.zoom = max(
            0.1,
            min(self.camera.zoom, 5.0)
        )

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_MIDDLE:
            self.dragging = True

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_MIDDLE:
            self.dragging = False

    def on_mouse_motion(self, x, y, dx, dy):
        if not self.dragging:
            return

        self.camera.position = (
            self.camera.position[0] - dx / self.camera.zoom,
            self.camera.position[1] - dy / self.camera.zoom
        )

    def get_zone_color(self, zone):
        color = zone.get_color()

        if isinstance(color, (tuple, list)):
            return color

        return getattr(
            arcade.color,
            color.upper(),
            arcade.color.WHITE
        )

    def on_draw(self):
        self.clear()

        if not self.turns:
            return

        self.camera.use()

        active_turn_dict = self.turns[self.current_turn]

        for connection in self.graph.connections:
            name1, name2 = connection.get_zones()

            if name1 not in self.zone_position or name2 not in self.zone_position:
                continue

            x1, y1 = self.zone_position[name1]
            x2, y2 = self.zone_position[name2]

            arcade.draw_line(
                x1,
                y1,
                x2,
                y2,
                arcade.color.WHITE,
                4
            )

        for zone_name, drone_ids in active_turn_dict.items():
            if zone_name not in self.zone_position:
                continue

            zone_x, zone_y = self.zone_position[zone_name]
            zone = self.graph.zones[zone_name]

            arcade.draw_circle_filled(
                zone_x,
                zone_y,
                30,
                self.get_zone_color(zone)
            )

            arcade.draw_circle_outline(
                zone_x,
                zone_y,
                30,
                arcade.color.WHITE,
                border_width=2
            )

            arcade.draw_text(
                zone_name,
                zone_x,
                zone_y + 45,
                arcade.color.LIGHT_GRAY,
                12,
                anchor_x="center"
            )

            for index, drone_id in enumerate(drone_ids):
                offset = index * 5
                drone_x = zone_x + offset
                drone_y = zone_y + offset

                arcade.draw_circle_filled(
                    drone_x,
                    drone_y,
                    13,
                    arcade.color.BATTLESHIP_GREY
                )

                arcade.draw_circle_outline(
                    drone_x,
                    drone_y,
                    13,
                    arcade.color.WHITE,
                    border_width=1
                )

                arcade.draw_text(
                    str(drone_id),
                    drone_x,
                    drone_y,
                    arcade.color.BLACK,
                    10,
                    anchor_x="center",
                    anchor_y="center",
                    bold=True
                )

        self.gui_camera.use()

        arcade.draw_text(
            f"Turn: {self.current_turn} / {len(self.turns) - 1}",
            20,
            SCREEN_HEIGHT - 40,
            arcade.color.WHITE,
            18
        )

        arcade.draw_text(
            "UP/DOWN: turns    WASD: move    Scroll: zoom    Middle Mouse: drag    R: reset",
            20,
            20,
            arcade.color.WHITE,
            14
        )

