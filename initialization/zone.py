class Zone():
    def __init__(self, zone_type, name, x, y, zone,color="white", max_drones=1):
        self.zone_type = zone_type
        self.name = name
        self.x = x
        self.y = y
        self.color = color
        self.max_drones = max_drones
        self.behavior = zone

    def get_movement_cost(self):
        self.behavior.get_movement_cost()

    def is_traversable(self):
        self.behavior.is_traversable()

    def get_capacity_limit(self, max_capacity):
        self.behavior.get_capacity_limit(max_capacity)
    

    def get_name(self):
        return self.name

    def get_coordinates(self):
        return (self.x, self.y)

    def get_color(self):
        return self.color

    def get_max_drones(self):
        return self.max_drones

