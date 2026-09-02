from abc import ABC, abstractmethod

class ZoneBehavior(ABC):
    """Strategy interface defining zone-type-specific traversal rules."""
    @abstractmethod
    def get_movement_cost(self) -> int:
        """Return the turn cost to move into a zone of this type."""

    @abstractmethod
    def is_traversable(self) -> bool:
        """Return whether a drone may enter a zone of this type."""

    @abstractmethod
    def get_capacity_limit(self, max_capacity: int) -> float:
        """Return the effective capacity limit given the configured max."""

    @abstractmethod
    def is_prior(self) -> bool:
        """Return the turn cost to move into a zone of this type."""


class NormalBehavior(ZoneBehavior):
    """Standard zone: 1 turn cost, traversable, uses configured capacity."""
    def get_movement_cost(self) -> int:
        return 1

    def is_traversable(self) -> bool:
        return True

    def get_capacity_limit(self, max_capacity: int) -> float:
        return max_capacity

    def is_prior(self) -> bool:
        return False

class RestrictedBehavior(ZoneBehavior):
    """Restricted zone: 2 turn cost, traversable, uses configured capacity."""
    def get_movement_cost(self) -> int:
        return 2

    def is_traversable(self) -> bool:
        return True

    def get_capacity_limit(self, max_capacity: int) -> float:
        return max_capacity

    def is_prior(self) -> bool:
        return False

class PriorityBehavior(ZoneBehavior):
    """Priority zone: 1 turn cost, traversable, preferred in pathfinding."""
    def get_movement_cost(self) -> int:
        return 1

    def is_traversable(self) -> bool:
        return True

    def get_capacity_limit(self, max_capacity: int) -> float:
        return max_capacity

    def is_prior(self) -> bool:
        return True

class BlockedBehavior(ZoneBehavior):
    """Blocked zone: not traversable, zero capacity."""
    def get_movement_cost(self) -> int:
        return 1

    def is_traversable(self) -> bool:
        return False

    def get_capacity_limit(self, max_capacity: int) -> float:
        return 0

    def is_prior(self) -> bool:
        return False

class StartZoneBehavior(ZoneBehavior):
    """Start zone: free entry, unlimited capacity."""
    def get_movement_cost(self) -> int:
        return 0

    def is_traversable(self) -> bool:
        return True

    def get_capacity_limit(self, max_capacity: int) -> float:
        return float('inf')

    def is_prior(self) -> bool:
        return False


class EndZoneBehavior(ZoneBehavior):
    """End zone: normal entry cost, unlimited capacity."""
    def get_movement_cost(self) -> int:
        return 0

    def is_traversable(self) -> bool:
        return True

    def get_capacity_limit(self, max_capacity: int) -> float:
        return float('inf')

    def is_prior(self) -> bool:
            return False