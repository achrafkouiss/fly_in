from abc import ABC, abstractmethod

class ZoneBehavior(ABC):
    @abstractmethod
    def get_movement_cost(self):
        pass

    @abstractmethod
    def is_traversable(self):
        pass

    @abstractmethod
    def get_capacity_limit(self, max_capacity):
        pass

class NormalBehavior(ZoneBehavior):
    def get_movement_cost(self):
        return 1

    def is_traversable(self):
        return True

    def get_capacity_limit(self, max_capacity):
        return max_capacity

class RestrictedBehavior(ZoneBehavior):
    def get_movement_cost(self):
        return 2

    def is_traversable(self):
        return True

    def get_capacity_limit(self, max_capacity):
        return max_capacity

class PriorityBehavior(ZoneBehavior):
    def get_movement_cost(self):
        return 1

    def is_traversable(self):
        return True

    def get_capacity_limit(self, max_capacity):
        return max_capacity

class BlockedBehavior(ZoneBehavior):
    def get_movement_cost(self):
        return 1

    def is_traversable(self):
        return False

    def get_capacity_limit(self, max_capacity):
        return 0

class StartZoneBehavior(ZoneBehavior):
    def get_movement_cost(self):
        return 0

    def is_traversable(self):
        return True

    def get_capacity_limit(self, max_capacity):
        return float('inf')


class EndZoneBehavior(ZoneBehavior):
    def get_movement_cost(self):
        return 1

    def is_traversable(self):
        return True

    def get_capacity_limit(self, max_capacity):
        return float('inf')