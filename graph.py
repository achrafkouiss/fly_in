from typing import Optional

from initialization import Zone, Connection


class Graph:
    """The full zone/connection network, with start and end zones resolved."""

    def __init__(self, zones: dict[str, Zone], connections: list[Connection]) -> None:
        """Initialize the graph, resolving start/end zones and adjacency.

        Args:
            zones: Mapping of zone name to Zone.
            connections: All Connection edges in the network.
        """
        self.zones = zones
        self.connections = connections
        self.start_zone = self._find_zone_by_type("start_hub")
        self.end_zone = self._find_zone_by_type("end_hub")
        self.adjacency: dict[str, list[Connection]] = self._build_adjacency()

    def _find_zone_by_type(self, zone_type: str) -> Zone:
        """Return the unique zone of the given type.

        The parser guarantees exactly one start_hub and one end_hub, so a
        missing match indicates a real bug upstream - raised loudly on
        purpose rather than silently returning None.
        """
        for zone in self.zones.values():
            if zone.zone_type == zone_type:
                return zone
        raise ValueError(f"no zone of type '{zone_type}' found in the network")

    def _build_adjacency(self) -> dict[str, list[Connection]]:
        """Build a name -> incident-connections lookup for every zone."""
        adjacency: dict[str, list[Connection]] = {name: [] for name in self.zones}
        for connection in self.connections:
            for name in connection.get_zones():
                adjacency[name].append(connection)
        return adjacency

    def get_neighbours(self, zone: Zone) -> list[Connection]:
        """Return the connections incident to the given zone."""
        return self.adjacency[zone.get_name()]

    def get_connection(self, zone1: Zone, zone2: Zone) -> Optional[Connection]:
        """Return the connection directly linking two zones, if any."""
        for connection in self.connections:
            if set(connection.get_zones()) == {zone1.get_name(), zone2.get_name()}:
                return connection
        return None

    def is_connected(self, start: Optional[str] = None, end: Optional[str] = None) -> bool:
        """Check reachability between zones via breadth-first search.

        Args:
            start: Name of the zone to search from. Defaults to the
                network's start zone.
            end: Name of the target zone. If omitted, checks whether
                every zone in the network is reachable from `start`.

        Returns:
            True if `end` is reachable from `start` (or, when `end` is
            omitted, if every zone is reachable from `start`).
        """
        start_name = start or self.start_zone.get_name()
        if start_name not in self.zones:
            raise ValueError(f"unknown zone '{start_name}'")

        visited = {start_name}
        queue = [start_name]
        while queue:
            current = queue.pop(0)
            if end is not None and current == end:
                return True
            for connection in self.adjacency[current]:
                neighbour = connection.get_other_zone(current)
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)

        if end is not None:
            return end in visited
        return visited == set(self.zones.keys())