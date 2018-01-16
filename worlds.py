"""
worlds.py
highwind

A collection of different worlds in which to run the simulation.
TODO: add more information to each space of the world
    What's the temperature?
    Is there ambient energy there?
"""

from random import randint
from queue import Queue

from . import organisms
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

def is_organism(subject):
    return issubclass(type(subject), organisms.Protozoa)


class BaseWorld():
    """The base class for worlds in which the organisms live.

    Params:
        dimensions - a tuple representing the dimensions of the world in width/height
        organisms - a list of the organisms living in that world
        display_type - the method of feedback by which the world interacts with
            the user, described as a string; the following options are available:

            "curses": if this option is chosen, the parameter "window" is also
                expected, containing a window object from the curses python module."""
    def __init__(self, dimensions = (11, 7), organisms = [], display_type = None, window = None):
        self.width = dimensions[0]
        self.height = dimensions[1]
        # TODO: Abstract grid and grid spaces into metadata classes
        self.grid = [StaticObjects.EMPTY] * (self.width * self.height)
        self.organisms = {}
        self.display_type = display_type
        self.print_queue = Queue()

        self.add_organisms(organisms)

        if self.display_type is "curses":
            # TODO: determine whether the window contains a curses window
            if window is None:
                raise ValueError("'window' must contain a valid curses window " + \
                                 "whenever the display_type is set to 'curses'.")
            else:
                self.window = window

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
                elif move is Moves.LEFT:
                    o.rotate(Directions.COUNTER_CLOCKWISE)
                elif move is Moves.RIGHT:
                    o.rotate(Directions.CLOCKWISE)
                elif move is Moves.EAT:
                    pass # TODO
                if o.alive:
                    living_organisms += 1
            if living_organisms is 0:
                return 0
        return living_organisms

    def console_print(self, string):
        """Queues up a string to be printed to the user's console."""
        self.print_queue.put(string)

    def show(self):
        """Updates the window in which the world is represented."""
        if self.display_type is "curses":
            self.show_curses()
        elif self.display_type is "text":
            self.show_text()

    def show_curses(self):
        # TODO: draw boundaries around the playing area
        for row in range(self.height):
            for col in range(self.width):
                obj = self.grid[col + (row * self.width)]
                # TODO: once spaces in the grid are their own class,
                # we can represent other objects, too.
                representation = ' '
                if is_organism(obj):
                    representation = str(obj)[0]
                self.window.addch(row, col, representation)
        line_no = self.height
        while not self.print_queue.empty():
            self.window.addstr(line_no, 0, self.print_queue.get())
            line_no += 1
        self.window.refresh()

# TODO: def show_text(self):

    def relocate_by_direction(self, index, direction, distance = 1):
        """Takes a location and moves it that direction distance spaces.

        Returns true on success, and false otherwise."""
        dest = index
        if direction == Directions.EAST:
            dest += 1
        elif direction == Directions.WEST:
            dest -= 1
        elif direction == Directions.NORTH:
            dest -= self.width
        elif direction == Directions.SOUTH:
            dest += self.width

        success = False
        try:
            if dest >= 0 and self.grid[dest] == StaticObjects.EMPTY:
                # if this is an organism, keep track of its location
                if is_organism(self.grid[index]):
                    self.organisms[self.grid[index]] = dest
                self.grid[dest] = self.grid[index]
                self.grid[index] = StaticObjects.EMPTY
                success = True
        except IndexError:
            pass

        return success

    def find_empty_space(self):
        """Locates an empty space on the grid."""
        # TODO: this should be moved to the grid object, when it exists
        increment = 1
        base_location = location = randint(0, len(self.grid) - 1)
        while self.grid[location] != StaticObjects.EMPTY:
            location = (base_location + increment**2) % len(self.grid)
            increment += 2

        return location

    def add_object(self, obj):
        """Places an object in an empty grid space."""
        location = self.find_empty_space()
        self.grid[location] = obj

    def add_organisms(self, organisms):
        """Adds each organism somewhere to the grid, and tracks that location."""
        for organism in organisms:
            location = self.find_empty_space()
            self.grid[location] = organism
            self.organisms[organism] = location
