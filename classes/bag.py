import math
from .constraint import Constraint
from functools import reduce

class Bag(object):
    ALMOST_FULL = 0.9

    def __init__(self, name, capacity):
        # Name of bag
        self.name = name
        # Maximum weight of bag
        self.capacity = int(capacity)
        # Items in the bag
        self.items = []
        # Constraints of bags
        self.constraints = []

    def __weight(self, weight, item):
        return item.weight + weight

    def __total_weight(self):
        return reduce(self.__weight, self.items, 0)

    def is_ninety_percent_full(self):
        weight = self.__total_weight()
        if math.floor(self.capacity * Bag.ALMOST_FULL) <= weight:
            return True
        return False

    def in_capacity(self, item):
        weight = self.__total_weight()
        if item.weight + weight <= self.capacity:
            # The bag is not full
            if not self.__fit_upper_limit(item):
                return False
            return True
        return False

    def __fit_upper_limit(self, item):
        for constraint in self.constraints:
            # Validate number of items in the bag
            self.items.append(item)
            result = constraint.bag_fit_limit()
            self.items.remove(item)
            if result == Constraint.BAG_ITEM_TOO_MUCH:
                return False
        return True


    def fit_lower_limit(self):
        for constraint in self.constraints:
            # Validate number of items in the bag
            result = constraint.bag_fit_limit()
            if result == Constraint.BAG_ITEM_NOT_ENOUGH:
                return False
        return True

    def __eq__(self, other):
        if isinstance(other, Bag):
            return self.name == other.name
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result
