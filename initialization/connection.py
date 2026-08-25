class Connection:
    def __init__(self, zone1, zone2, max_link_capacity=1):
        self.zone1 = zone1
        self.zone2 = zone2
        self.max_link_capacity = 1 if max_link_capacity is None else max_link_capacity

    def get_zones(self):
        return (self.zone1, self.zone2)

    def get_capacity(self):
        return self.max_link_capacity

    # def get_other_zone(self, zones):
    #     pass
