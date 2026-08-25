from initialization import Zone, Connection

class Graph:
    def __init__(self, zones: dict[str, Zone], connections: list[Connection]):
        self.zones = zones
        self.connections = connections
        self.start_zone = self.get_start_zone()
        self.end_zone = self.get_end_zone()
    

    def get_start_zone(self):
        for obj in self.zones.values():
            if getattr(obj, 'zone_type', None) == 'start_hub':
                return obj


    def get_end_zone(self):
        for obj in self.zones.values():
            if getattr(obj, 'zone_type', None) == 'end_hub':
                return obj
