import arcade

# --- Configuration ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Drone Zone Visualizer"

# Map your zone keys to explicit (x, y) screen coordinates
ZONE_POSITIONS = {
    "Zone_A": (200, 450),
    "Zone_B": (600, 450),
    "Zone_C": (200, 150),
    "Zone_D": (600, 150),
}

# --- Sample Data Structure ---
# A tuple of dicts: each dict is a turn, key = zone, value = list of drone IDs
TURN_DATA = (
    {"Zone_A":[1,2,3,4], "Zone_B":[], "Zone_C": [], "Zone_D": []},
    {"Zone_A":[], "Zone_B":[1,3], "Zone_C":[2,4], "Zone_D": []},
    # {"Zone_A": [], "Zone_B":[1], "Zone_C":[], "Zone_D": [2]},
    {"Zone_A":[], "Zone_B": [], "Zone_C":[], "Zone_D": [1, 2,3, 4]},
)

class DroneVisualizer(arcade.Window):
    def __init__(self, title, data):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, title)
        arcade.set_background_color(arcade.color.AMAZON)
        
        self.turns = data
        self.current_turn = 0
        self.time_since_last_turn = 0.0
        self.turn_duration = 1.5  # Seconds to hold each turn

    # def on_update(self, delta_time: float):
    #     # Track time to advance the turns automatically
    #     self.time_since_last_turn += delta_time
    #     if self.time_since_last_turn >= self.turn_duration:
    #         self.time_since_last_turn = 0.0
    #         # Loop back to turn 0 when the data ends
    #         self.current_turn = (self.current_turn + 1) % len(self.turns)

def on_key_press(self, key, modifiers):
    if key == arcade.key.RIGHT:
        # Next turn
        if self.current_turn < len(self.turns) - 1:
            self.current_turn += 1

    elif key == arcade.key.LEFT:
        # Previous turn
        if self.current_turn > 0:
            self.current_turn -= 1
    def on_draw(self):
        self.clear()
        
        # 1. Draw the current turn HUD info
        arcade.draw_text(
            f"Turn: {self.current_turn + 1} / {len(self.turns)}",
            20, SCREEN_HEIGHT - 40, arcade.color.WHITE, 18
        )

        # 2. Get the dictionary for the current turn
        active_turn_dict = self.turns[self.current_turn]

        # 3. Iterate through your data structure and draw
        for zone_name, drone_ids in active_turn_dict.items():
            if zone_name not in ZONE_POSITIONS:
                continue
                
            # Get the center position of the zone
            zone_x, zone_y = ZONE_POSITIONS[zone_name]

            # Draw the visual boundary for the zone
            # arcade.draw_rectangle_outline(
            #     zone_x, zone_y, 250, 200, arcade.color.WHITE, 2
            # )
            arcade.draw_circle_filled(zone_x, zone_y, 30, arcade.color.SKY_BLUE, 0)
            arcade.draw_circle_outline(zone_x, zone_y, 30, arcade.color.WHITE, border_width=1, tilt_angle=0, num_segments=-1)
            arcade.draw_text(
                zone_name, zone_x - 115, zone_y + 75, arcade.color.LIGHT_GRAY, 12
            )

            # Draw the drones inside this zone (staggered so they don't overlap)
            for index, drone_id in enumerate(drone_ids):
                # Offset each drone slightly inside the box
                drone_x = zone_x - 80 + (index * 50)
                drone_y = zone_y

                # Draw drone body
                arcade.draw_circle_filled(
                    drone_x, drone_y, 15, arcade.color.BATTLESHIP_GREY
                )
                # Draw drone ID label
                arcade.draw_text(
                    str(drone_id), drone_x - 5, drone_y - 6, arcade.color.BLACK, 11, bold=True
                )

def main():
    window = DroneVisualizer(SCREEN_TITLE, TURN_DATA)
    arcade.run()

if __name__ == "__main__":
    main()


# import arcade


# WIDTH = 1000
# HEIGHT = 700


# class Viewer(arcade.Window):

#     def __init__(self):
#         super().__init__(WIDTH, HEIGHT, "Drone Simulation")

#         self.zones = {
#             "start": (100, 350),
#             "zone_a": (300, 500),
#             "zone_b": (300, 200),
#             "zone_c": (550, 350),
#             "end": (800, 350),
#         }

#         self.connections = [
#             ("start", "zone_a"),
#             ("start", "zone_b"),
#             ("zone_a", "zone_c"),
#             ("zone_b", "zone_c"),
#             ("zone_c", "end"),
#         ]

#         self.turns = (
#             {
#                 "start": ["D1", "D2"],
#                 "zone_a": ["D3"],
#             },
#             {
#                 "zone_a": ["D1", "D2"],
#                 "zone_c": ["D3"],
#             },
#             {
#                 "zone_c": ["D1", "D2", "D3"],
#             },
#             {
#                 "end": ["D1", "D2", "D3"],
#             },
#         )

#         self.current_turn = 0

#     def on_draw(self):
#         self.clear()

#         # Connections
#         for zone1, zone2 in self.connections:
#             x1, y1 = self.zones[zone1]
#             x2, y2 = self.zones[zone2]

#             arcade.draw_line(x1, y1, x2, y2, 2)

#         # Zones
#         for name, (x, y) in self.zones.items():

#             arcade.draw_circle_outline(x, y, 40, 2)

#             arcade.draw_text(
#                 name,
#                 x,
#                 y - 65,
#                 font_size=14,
#                 anchor_x="center"
#             )

#         # Drones
#         state = self.turns[self.current_turn]

#         for zone_name, drones in state.items():

#             x, y = self.zones[zone_name]

#             for i, drone_id in enumerate(drones):

#                 drone_x = x + (i - len(drones) / 2) * 20
#                 drone_y = y

#                 arcade.draw_circle_filled(
#                     drone_x,
#                     drone_y,
#                     8
#                 )

#                 arcade.draw_text(
#                     drone_id,
#                     drone_x,
#                     drone_y + 12,
#                     font_size=10,
#                     anchor_x="center"
#                 )

#         # Turn
#         arcade.draw_text(
#             f"Turn {self.current_turn + 1}",
#             20,
#             HEIGHT - 40,
#             font_size=22
#         )


# Viewer().run()