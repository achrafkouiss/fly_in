from typing import Optional, Union

from parsing import MainParser, SourceReader
from initialization import ZoneFactory, ConnectionFactory, Drone
from graph import Graph
from pathfinder import Pathfinder
from simulation import Simulation



class Network:
    """Wires together parsing, zone/connection construction, and the graph."""

    def __init__(self) -> None:
        """Initialize the factories and their keyword dispatch table."""
        self.zone_factory = ZoneFactory()
        # print(type(self.zone_factory.zones))
        self.connection_factory = ConnectionFactory(self.zone_factory.zones)
        self.dispatch: dict[str, Union[ZoneFactory, ConnectionFactory]] = {
            "connection": self.connection_factory,
            "start_hub": self.zone_factory,
            "hub": self.zone_factory,
            "end_hub": self.zone_factory,
        }
        # self.nb_drones: Optional[int] = None
        # self.graph: Optional[Graph] = None

    def start(self, file_name: str) -> Graph:
        reader = SourceReader(file_name)
        parsing = MainParser()
        lines = parsing.check_grammar(reader.read_lines())

        nb_drones = lines[0][2]
        for line in lines[1:]:
            self.dispatch[line[1]].builder(line)
        zones = self.zone_factory.zones
        connections = self.connection_factory.connections
        graph = Graph(zones, connections)
        visited_zones = graph.is_connected()
        if len(visited_zones) != len(zones):
            diff = zones.keys() - visited_zones
            raise ValueError(f"{' '.join(diff)} these zones are disconnected from the from the graph")
        pathfinder = Pathfinder(graph, nb_drones, 1)
        paths = pathfinder.find_all_paths()
        print(paths)
        drones = []
        for i in range(nb_drones):
            drone = Drone(
                i + 1,
                paths[i]
            )
            drones.append(drone)
        simulation = Simulation(drones, graph)
        simulation.run()
        return graph


if __name__ == "__main__":
    network = Network()
    # maps\medium\01_dead_end_trap.txt
    # maps\medium\02_circular_loop.txt
    graph = network.start("maps/medium/02_circular_loop.txt")
    # print(f"drones: {network.nb_drones}")
    # print(f"start: {graph.start_zone.get_name()}, end: {graph.end_zone.get_name()}")