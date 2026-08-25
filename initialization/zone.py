from .zone_behavior import ZoneBehavior


class Zone:
    """Represents a single zone (node) in the drone routing graph."""

    def __init__(
        self,
        zone_type: str,
        name: str,
        x: int,
        y: int,
        behavior: ZoneBehavior,
        color: str = "white",
        max_drones: int = 1,
    ) -> None:
        """Initialize a Zone.

        Args:
            zone_type: The kind of zone ("hub", "start_hub", "end_hub").
            name: Unique zone name.
            x: X coordinate.
            y: Y coordinate.
            behavior: Strategy object defining movement/capacity rules.
            color: Display color (default "white").
            max_drones: Maximum simultaneous drone occupancy (default 1).
        """
        self.zone_type = zone_type
        self.name = name
        self.x = x
        self.y = y
        self.color = color
        self.max_drones = max_drones
        self.behavior = behavior

    def get_movement_cost(self) -> int:
        """Return the turn cost of moving into this zone."""
        return self.behavior.get_movement_cost()

    def is_traversable(self) -> bool:
        """Return whether drones may enter this zone."""
        return self.behavior.is_traversable()

    def get_capacity_limit(self, max_capacity: int) -> float:
        """Return the effective capacity limit for this zone.

        Note:
            For start/end zones this always returns infinity regardless of
            any max_drones metadata, per the subject's occupancy rules.
        """
        return self.behavior.get_capacity_limit(max_capacity)

    def get_name(self) -> str:
        """Return the zone's name."""
        return self.name

    def get_coordinates(self) -> tuple[int, int]:
        """Return the (x, y) coordinates of the zone."""
        return (self.x, self.y)

    def get_color(self) -> str:
        """Return the display color of the zone."""
        return self.color

    def get_max_drones(self) -> int:
        """Return the configured max drone capacity (raw metadata value)."""
        return self.max_drones