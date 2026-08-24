from zone_behavior import NormalBehavior, BlockedBehavior, PriorityBehavior, \
    RestrictedBehavior, EndZoneBehavior, StartZoneBehavior
from zone import Zone

class ZoneFactory():
    def __init__(self):
        self.zones_behaviour = {
                "normal": NormalBehavior(),
                "blocked": BlockedBehavior(),
                "priority": PriorityBehavior(),
                "restricted": RestrictedBehavior(),
                "start_hub": StartZoneBehavior(),
                "end_hub": EndZoneBehavior(),
                }
        self.zones: dict = {}

    def get_behavior(self, behavior, zone_type):
        if not behavior and zone_type == 'hub':
            behavior = "normal"
        elif behavior and zone_type == 'hub':
            pass
        else:
            behavior = zone_type
        return self.zones_behaviour[behavior]

    def check_replicated(self, name, x, y,line):
        # print(name , self.zones.get(name))
        if self.zones.get(name):
            raise ValueError(f"line {line}: the zone name {name} is duplicated")
        for obj in self.zones.values():
            coord = (obj.x, obj.y)
            if coord == (x, y):
                raise ValueError(f"line {line}: the zone cordinates {coord} is duplicated")

    def zone_builder(self, line):
        zone_type = line[1]
        name = line[2]
        x = line[3]
        y = line[4]
        options = line[5] if len(line) > 5 else {}
        color = options.get("color")
        max_drones = options.get("max_drones")
        zone = self.get_behavior(options.get("zone"), zone_type)
        self.check_replicated(name, x, y, line[0])
        new_zone = Zone(
            zone_type,
            name,
            x,
            y,
            color,
            max_drones,
            zone
        )
        self.zones[name] = new_zone




if __name__ == "__main__":
    a = ZoneFactory()
    a.zone_builder((6, 'hub', 'waypoint1', 2, 0, {'zone': 'priority', 'color': 'green', 'max_drones': '2'}))
    a.zone_builder((6, 'hub', 'waypoint2', 3, 0, {'zone': 'priority', 'color': 'green', 'max_drones': '2'}))

    