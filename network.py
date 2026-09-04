from typing import Optional, Union

from parsing import MainParser, SourceReader
from initialization import ZoneFactory, ConnectionFactory, Drone
from graph import Graph
from pathfinder import Pathfinder
from simulation import Simulation
from visualization2 import DroneVisualizer

import arcade

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
        pathfinder = Pathfinder(graph, nb_drones, 0.01)
        paths = pathfinder.find_all_paths()
        # print(paths)
        drones = []
        for i in range(nb_drones):
            drone = Drone(
                i + 1,
                paths[i]
            )
            drones.append(drone)
        simulation = Simulation(drones, graph)
        simulation.run()
        print(simulation.get_history())
        window = DroneVisualizer(graph, simulation.get_history())
        arcade.run()

        # for penalty in [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0,0.1, 0.2, 0.3, 0.4, 0,5, 1, 1.5, 2, 2.5, 3, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10]:
        #     pathfinder = Pathfinder(graph, nb_drones, penalty)
        #     paths = pathfinder.find_all_paths()
        #     drones = []
        #     for i in range(nb_drones):
        #         drone = Drone(
        #             i + 1,
        #             paths[i]
        #         )
        #         drones.append(drone)
        #     simulation = Simulation(drones, graph)
        #     turns = simulation.run()
        #     print(f"Penalty {penalty}: {simulation.turn_counter} turns")
        return graph


if __name__ == "__main__":
    network = Network()
    # maps/easy/01_linear_path.txt
    # maps/easy/02_simple_fork.txt
    # maps/easy/03_basic_capacity.txt
    # maps/medium/01_dead_end_trap.txt
    # maps/medium/02_circular_loop.txt
    # maps/medium/03_priority_puzzle.txt
    # maps/hard/01_maze_nightmare.txt
    # maps/hard/02_capacity_hell.txt
    # maps/hard/03_ultimate_challenge.txt

    # maps/challenger/01_the_impossible_dream.txt

    # graph = network.start("maps/easy/01_linear_path.txt")
    # graph = network.start("maps/easy/02_simple_fork.txt")
    # graph = network.start("maps/easy/03_basic_capacity.txt")

    # graph = network.start("maps/medium/01_dead_end_trap.txt")
    # graph = network.start("maps/medium/02_circular_loop.txt")
    # graph = network.start("maps/medium/03_priority_puzzle.txt")

    # graph = network.start("maps/hard/01_maze_nightmare.txt")
    # graph = network.start("maps/hard/02_capacity_hell.txt")
    # graph = network.start("maps/hard/03_ultimate_challenge.txt")

    graph = network.start("maps/challenger/01_the_impossible_dream.txt")
    # print(f"drones: {network.nb_drones}")
    # print(f"start: {graph.start_zone.get_name()}, end: {graph.end_zone.get_name()}")