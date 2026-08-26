from typing import Optional, Union

from parsing import MainParser, SourceReader
from initialization import ZoneFactory, ConnectionFactory
from graph import Graph


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

        self.nb_drones = lines[0][2]
        for line in lines[1:]:
            self.dispatch[line[1]].builder(line)

        self.graph = Graph(self.zone_factory.zones, self.connection_factory.connections)
        return self.graph


if __name__ == "__main__":
    network = Network()
    graph = network.start("maps/easy/01_linear_path.txt")
    # print(f"drones: {network.nb_drones}")
    # print(f"start: {graph.start_zone.get_name()}, end: {graph.end_zone.get_name()}")