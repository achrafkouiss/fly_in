from typing import Optional


class Connection:
    """Represents a bidirectional edge between two zones."""

    def __init__(
        self, name1: str, name2: str, max_link_capacity: Optional[int] = None
    ) -> None:
        """Initialize a Connection.

        Args:
            name1: Name of the first endpoint zone.
            name2: Name of the second endpoint zone.
            max_link_capacity: Max drones that may traverse simultaneously.
                Defaults to 1 when not specified in the map file.
        """
        self.name1 = name1
        self.name2 = name2
        self.max_link_capacity = 1 if max_link_capacity is None else max_link_capacity

    def get_zones(self) -> tuple[str, str]:
        """Return the (name1, name2) endpoint names of this connection."""
        return (self.name1, self.name2)

    def get_capacity(self) -> int:
        """Return the max number of drones allowed to traverse at once."""
        return self.max_link_capacity

    def get_other_zone(self, name: str) -> str:
        """Return the endpoint name on the opposite side of `name`."""
        if name == self.name1:
            return self.name2
        if name == self.name2:
            return self.name1
        raise ValueError(f"'{name}' is not part of this connection")