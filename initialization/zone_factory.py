from typing import Optional

from .zone_behavior import (
    NormalBehavior,
    BlockedBehavior,
    PriorityBehavior,
    RestrictedBehavior,
    EndZoneBehavior,
    StartZoneBehavior,
    ZoneBehavior,
)
from .zone import Zone


class ZoneFactory:
    """Builds Zone objects from parsed line tuples, attaching the right behavior."""

    def __init__(self) -> None:
        """Initialize the factory with the available behavior strategies."""
        self.zones_behaviour: dict[str, ZoneBehavior] = {
            "normal": NormalBehavior(),
            "blocked": BlockedBehavior(),
            "priority": PriorityBehavior(),
            "restricted": RestrictedBehavior(),
            "start_hub": StartZoneBehavior(),
            "end_hub": EndZoneBehavior(),
        }
        self.zones: dict[str, Zone] = {}

    def get_behavior(self, behavior_name: Optional[str], zone_type: str) -> ZoneBehavior:
        """Resolve the ZoneBehavior to attach to a zone."""
        if zone_type != "hub":
            return self.zones_behaviour[zone_type]
        return self.zones_behaviour[behavior_name or "normal"]

    def check_replicated(self, name: str, x: int, y: int, line_number: int) -> None:
        """Raise if a zone with this name or these coordinates already exists."""
        if name in self.zones:
            raise ValueError(f"line {line_number}: the zone name {name} is duplicated")
        for zone in self.zones.values():
            if zone.get_coordinates() == (x, y):
                raise ValueError(
                    f"line {line_number}: the zone cordinates {(x, y)} is duplicated"
                )

    def builder(self, line: tuple) -> Zone:
        """Build a Zone from a parsed line tuple and register it.

        Args:
            line: Tuple of (line_number, zone_type, name, x, y, [metadata]).

        Returns:
            The newly built Zone.
        """
        line_number, zone_type, name, x, y = line[0], line[1], line[2], line[3], line[4]
        options = line[5] if len(line) > 5 else {}
        color = options.get("color", "white")
        max_drones = options.get("max_drones", 1)
        behavior = self.get_behavior(options.get("zone"), zone_type)

        self.check_replicated(name, x, y, line_number)

        new_zone = Zone(zone_type, name, x, y, behavior, color, max_drones)
        self.zones[name] = new_zone
        return new_zone


if __name__ == "__main__":
    factory = ZoneFactory()
    factory.builder(
        (6, "hub", "waypoint1", 2, 0, {"zone": "priority", "color": "green", "max_drones": 2})
    )
    factory.builder(
        (6, "hub", "waypoint2", 3, 0, {"zone": "priority", "color": "green", "max_drones": 2})
    )