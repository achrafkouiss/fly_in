from .connection import Connection


class ConnectionFactory:
    """Builds Connection objects, validating them against known zones."""

    def __init__(self, zones: dict) -> None:
        """Store a reference to the (shared) zones dict for existence checks.

        Args:
            zones: The ZoneFactory's zones dict. Kept by reference so that
                connections built after more zones are added still see them.
        """
        self.zones = zones
        self.connections: list[Connection] = []

    def builder(self, line: tuple) -> Connection:
        """Build a Connection from a parsed line tuple and register it.

        Args:
            line: Tuple of (line_number, 'connection', (name1, name2), [metadata]).

        Returns:
            The newly built Connection.
        """
        line_number = line[0]
        name1, name2 = line[2]
        if name1 not in self.zones or name2 not in self.zones:
            raise ValueError(
                f"line {line_number}: make sure zones exist before making the connection"
            )
        options = line[3] if len(line) > 3 else {}
        max_link_capacity = options.get("max_link_capacity")
        connection = Connection(name1, name2, max_link_capacity)
        self.connections.append(connection)
        return connection