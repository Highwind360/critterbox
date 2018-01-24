"""
constants.py
highwind

A collection of all the constant values.
"""

from enum import Enum


# TODO: attack, defend
class Moves(Enum):
    DEAD = -1
    WAIT = 0
    LEFT = 1
    RIGHT = 2
    FORWARD = 3
    EAT = 4
    DRINK = 5


class Directions(Enum):
    EAST = 0
    NORTH = 1
    WEST = 2
    SOUTH = 3


# The order in which cardinal directions would be traversed moving counterclockwise
ORDER_OF_CARDINAL_DIRECTIONS = [
    Directions.EAST,
    Directions.NORTH,
    Directions.WEST,
    Directions.SOUTH
]
