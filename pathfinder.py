import heapq
from graph import Graph

class Pathfinder():
    def __init__(self, graph, num_drones, penalty_amount):
        self.graph = graph
        self.dynamic_costs = self.set_dynamic_costs()
        self.num_drones = num_drones
        self.penalty_amount = penalty_amount
        

    def set_dynamic_costs(self):
        dynamic_costs = {zone_name: 0 for zone_name in self.graph.zones.keys()}
        return dynamic_costs

    def find_single_path(self, zones, start_zone, end_zone):
        distances = {node: float('inf') for node in zones}
        distances[start_zone.get_name()] = 0
    
        priority_count = {node: 0 for node in zones}
    
        pq = [(0, start_zone.get_name())]

        previous = {node: None for node in zones}

        while pq:
            current_distance, current_node = heapq.heappop(pq)

            if current_node == end_zone.get_name():
                break

            if current_distance > distances[current_node]:
                continue

            for connection in self.graph.get_neighbours(zones[current_node]):
                neighbor = connection.get_other_zone(current_node)

                if not zones[neighbor].is_traversable():
                    continue

                base_weight = zones[neighbor].get_movement_cost()
                dynamic_adjustment = self.dynamic_costs.get(neighbor, 0)
                weight = base_weight + dynamic_adjustment

                distance = current_distance + weight

                new_priority_count = priority_count[current_node]

                if zones[neighbor].is_prior():
                    new_priority_count += 1
    
                if (
                    distance < distances[neighbor]
                    or (
                        distance == distances[neighbor]
                        and new_priority_count > priority_count[neighbor]
                        )
                        ):
                    distances[neighbor] = distance
                    priority_count[neighbor] = new_priority_count
                    previous[neighbor] = current_node

                    heapq.heappush(
                        pq,
                        (distance, neighbor)
                        )
        # print(previous)
        path = []
        current = end_zone.get_name()
        if distances[end_zone.get_name()] == float('inf'):
            raise ValueError("no valid path has been found")
        while current is not None:
            path.insert(0, current)
            current = previous[current]
        return distances[end_zone.get_name()], path

    def update_dynamic_costs(self, path):
        for zone_name in self.graph.zones.keys():
            # print("zone name = ", zone_name, "\npath = ", path)

            # print("\n\n")
            if zone_name in path and zone_name not in (self.graph.start_zone.get_name(), self.graph.end_zone.get_name()):
                self.dynamic_costs[zone_name] += self.penalty_amount
        # print(self.dynamic_costs)

    def find_all_paths(self):
        paths = []
        for _ in range(self.num_drones):
            _ , path = self.find_single_path(
                self.graph.zones,
                self.graph.start_zone,
                self.graph.end_zone
                )
            self.update_dynamic_costs(path)
            paths.append(path)
        return paths
            