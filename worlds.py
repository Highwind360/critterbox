"""
worlds.py
highwind

A collection of different worlds in which to run the simulation.
TODO: add more information to each space of the world
    What's the temperature?
    Is there ambient energy there?
"""

from random import randint

from .constants import StaticObjects, Directions, Moves


def get_cardinal_map(grid, x, y, width, height):
    """Using a given x and y coordinates on an array of length width * height,
    find what is located in the cardinal directions with respect to that organism.

    Returns this information as a dict of the form { Directions.NORTH: 'Wall' }"""
    directions = {}
    cur = x * y
    north, south, west, east = cur - width, cur + width, cur - 1, cur + 1
    cardinals = Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST
    for direction, coord in zip(cardinals, [north, south, east, west]):
        # if any of the directions are outside of the boundary of the grid,
        # mark them accordingly
        if coord < 0 or coord >= width * height:
            directions[direction] = StaticObjects.BOUNDARY
        else: # otherwise, just see what's there
            directions[direction] = grid[coord]
    return directions


class BaseWorld():
    """The base class for worlds in which the organisms live."""

    def __init__(self, dimensions = (11, 7), organisms = []):
        self.width = dimensions[0]
        self.height = dimensions[1]
        # TODO: Abstract grid and grid spaces into metadata classes
        self.grid = [StaticObjects.EMPTY] * (self.width * self.height)
        self.organisms = {}

        for organism in organisms:
            increment = 1
            base_location = location = randint(0, len(self.grid) - 1)
            while self.grid[location] != StaticObjects.EMPTY:
                location = (base_location + increment**2) % len(self.grid)
                increment += 2
            self.grid[location] = organism
            self.organisms[organism] = location

    def step(self, steplength = 1):
        """Takes a step steplength times or until all organisms have died.
        
        Returns the number of organisms currently alive."""
        for i in range(steplength):
            living_organisms = 0
            for o in self.organisms.keys():
                o_x, o_y = self.organisms[o] % self.width, self.organisms[o] // self.width
                environment = get_cardinal_map(self.grid, o_x, o_y, self.width, self.height)
                move = o.move(environment)
                if move is Moves.FORWARD:
                    self.relocate_by_direction(self.organisms[o], o.orientation)
                elif move in (Moves.LEFT, Moves.RIGHT):
                    pass # TODO
                elif move is Moves.EAT:
                    pass # TODO
                if o.alive:
                    living_organisms += 1
            if living_organisms is 0:
                return 0
        return living_organisms

    # TODO: relocate_by_direction(index, orientation, distance = 1)
    # TODO: add_organisms method
