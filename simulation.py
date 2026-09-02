

class Simulation:
    def __init__(self, drones, graph):
        self.drones = drones
        self.graph = graph
        self.turn_counter = 0
        self.occupancy = {zone: drones.copy() if zone == graph.start_zone.get_name() else [] for zone in graph.zones}
        self.turn_log = []
        self.connection_occupancy = {}
        # print(self.occupancy)
        # print(self.occupancy )

    def run(self):
        while any(not obj.has_reached_end() for obj in self.drones):
            # print([not obj.has_reached_end() for obj in self.drones])
            # print("self drones = ", self.drones)
            # print("self.occupancy = ", self.occupancy)
            # print("current_occupancy = ", {key: len(occ) for key, occ in self.occupancy.items()})
            self.connection_occupancy = {connection: [] for connection in self.graph.connections}
            # print("self.connection_occupancy = ", self.connection_occupancy)
            self.turn_counter += 1
            turn_movements = self.process_turn()

            if turn_movements:
                self.turn_log.append(" ".join(turn_movements))
            # if index == 3:
            #     import sys
            #     sys.exit()
            # index += 1
            # print("-----------------------------------------------------------------------")
        print(*self.turn_log, sep="\n")

    def process_turn(self):
        turn_movements = []
        ongoing_drones = [
            obj
            for obj in self.drones
            if not obj.has_reached_end()
            ]
        # print("ALL DRONES:", [(d.get_drone_id(), d.current_index, d.get_path())for d in self.drones])
        # print("ONGOING:", [(d.get_drone_id(), d.current_index, d.get_path()) for d in ongoing_drones])
        # print(ongoing_drones)
        for drone in ongoing_drones:
            current_zone = drone.get_current_zone()
            next_zone = drone.get_next_zone()
            connection = self.graph.get_connection(self.graph.zones[current_zone], self.graph.zones[next_zone])
            # print(f"        Drone {drone.get_drone_id()}")
            # print("current zone = ", current_zone)
            # print("next_zone zone = ", next_zone)
            if self.can_move(connection, next_zone):
                # print(current_zone)
                # print(self.graph.zones)
                if drone.movement_progress(self.graph.zones[drone.get_current_zone()].get_movement_cost() ):
                    self.update_connection_occupancy(connection, drone, "enter")
                    drone.move_to_next_zone()
                    # print(next_zone)
                    # print("self.graph.zones = ", self.graph.zones)
                    # if self.graph.zones[next_zone].get_movement_cost() != 2:
                    turn_movements.append(f"D{drone.get_drone_id()}-{next_zone}")
                    # else:
                    #     zone1, zone2 = connection.get_zones()
                    #     self.turn_log.append(f"D{drone.get_drone_id()}-{zone1} {zone2}")
                    self.update_occupancy(next_zone, drone, "enter")
                    self.update_occupancy(current_zone, drone, "leave")

            # else:
            #     self.turn_log.append(f"Drone {drone.get_drone_id()} waited")
        # print(self.connection_occupancy)
            # print("----------------------------------")
            # print("----------------------------------")
        return turn_movements



    def can_move(self, connection, next_zone):
        current_occupancy = self.occupancy[next_zone]
        available_capacity = self.graph.zones[next_zone].get_capacity_limit()
        # print("current_occupancy = ", [occ.get_drone_id() for occ in current_occupancy])
        # print("available_capacity = ", available_capacity)
        if len(current_occupancy) >= available_capacity:
            return False
        # connection = self.graph.get_connection(self.graph.zones[current_zone], self.graph.zones[next_zone])
        # print(connection)
        connection_occupancy = self.connection_occupancy[connection]
        # print("connection_occupancy = ", [occ.get_drone_id() for occ in connection_occupancy])
        
        # print("connection = ", connection.get_zones())
        # print("connection.get_capacity() = ", connection.get_capacity())
        if len(connection_occupancy) >= connection.get_capacity():
            # print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            return False
        return True

    def update_occupancy(self, zone, drone, action):
        # print("self.occupancy = ", self.occupancy)
        # print(f"self.occupancy[{zone}] = ", self.occupancy[zone])
        # print("self.drones = ", [drone.get_drone_id() for drone in self.drones])
        if action == "enter":
            # print(f"Drone {drone.get_drone_id()} enterd")
            self.occupancy[zone].append(drone)
            # print(self.occupancy[zone])
        elif action == "leave":
            # print(f"Drone {drone.get_drone_id()} leaved")
            self.occupancy[zone].remove(drone)

    def update_connection_occupancy(self, connection, drone, action):
        if action == "enter":
            # print(f"Drone {drone.get_drone_id()} enterd")
            self.connection_occupancy[connection].append(drone)
        elif action == "leave":
            # print(f"Drone {drone.get_drone_id()} leaved")
            self.connection_occupancy[connection].remove(drone)