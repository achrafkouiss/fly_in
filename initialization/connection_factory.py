from .connection import Connection

class ConnectionFactory:
    def __init__(self):
        self.connections = []

    def builder(self, line, zones):
        zone1, zone2 = line[2]
        if zone1 not in zones or zone2 not in zones:
            raise ValueError(f"line {line[0]}: make sure zones exist before making the connection")
        options = line[3] if len(line) > 3 else {}
        max_link_capacity = options.get("max_link_capacity")
        connection = Connection(
            zone1,
            zone2,
            max_link_capacity
        )
        self.connections.append(connection)
        return connection

        # new_zone = Zone(
        #     zone_type,
        #     name,
        #     x,
        #     y,
        #     zone,
        #     color,
        #     max_drones
        # )
        # self.zones[name] = new_zone