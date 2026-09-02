class Drone():
    def __init__(self, drone_id, path):
        self.drone_id = drone_id
        self.path = path
        self.current_index = 0
        self.status = 0
    
    def get_current_zone(self):
        return self.path[self.current_index]

    def get_next_zone(self):
        return self.path[self.current_index + 1]

    def move_to_next_zone(self):
        # print(f"Drone {self.drone_id}: " f"{self.current_index} -> {self.current_index + 1}" )
        self.current_index += 1
        self.status = 1
        return self.get_current_zone()

    def has_reached_end(self):
        # print(f"========> self.current_index = {self.current_index}")
        # print(f"========> len(self.path) = {len(self.path)}")
        # print(f"========> len(self.path) - 1 = {len(self.path) - 1}")
        return self.current_index == len(self.path) - 1

    def get_path(self):
        return self.path

    def get_drone_id(self):
        return self.drone_id

    def movement_progress(self, movement_cost):
        if self.status < movement_cost:
            self.status += 1
            return False
        else:
            return True