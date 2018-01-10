"""
constants.py
highwind

A collection of all the constant values.
"""

from enum import Enum


class Moves(Enum):
    DEAD = -1
    WAIT = 0
    LEFT = 1
    RIGHT = 2
    FORWARD = 3
    EAT = 4


class Directions(Enum):
    EAST = 0
    NORTH = 1
    WEST = 2
    SOUTH = 3


class StaticObjects(Enum):
    BOUNDARY = -1
    EMPTY = 0
    WALL = 1
