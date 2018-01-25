"""
worlds.py
highwind

A collection of different worlds in which to run the simulation.
"""

from queue import Queue
from random import randint
from functools import wraps

from . import static_objects
from .organisms import Protozoa
from .constants import Directions, Moves


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
            directions[direction] = GridSpace(is_boundary = True)
        else: # otherwise, just see what's there
            directions[direction] = grid[coord]
    return directions


class GridSpace():
    """A container for whatever is inside each space in the grid.

    Params:
        contents - a CritterBoxObject that the space contains"""
    # TODO: add more information to each space of the world
    #    What's the temperature?
    #    Is there ambient energy there?

    # TODO: make this a decorator
    def __check_is_cbo__(self, obj):
        """Validates whether something is a CritterBoxObject."""
        if (obj is not None and not
                isinstance(obj, static_objects.CritterBoxObject)):
            raise ValueError("Object must be a CritterBoxObject.")

    def return_false_if_boundary(func):
        @wraps(func)
        def function_wrapper(self, *args, **kwargs):
            if self.is_boundary:
                return False
            return func(self, *args, **kwargs)
        return function_wrapper

    def __init__(self, contents = None, is_boundary = False):
        self.__check_is_cbo__(contents)
        self.contents = contents
        self.is_boundary = is_boundary

    def empty(self):
        """Discard whatever this space was containing.

        Returns the contents."""
        c = self.contents
        self.contents = None
        return c

    def is_empty(self):
        """Returns whether this space contains nothing."""
        return not self.is_boundary and self.contents == None

    @return_false_if_boundary
    def put(self, obj):
        """Place an object into the space.

        Returns true on success"""
        self.__check_is_cbo__(obj)
        self.contents = obj
        return True

    @return_false_if_boundary
    def move_from(self, other_space):
        """Moves an object from another space to the current space.

        Returns true on success"""
        self.put(other_space.empty())
        return True

    @return_false_if_boundary
    def contains_organism(self):
        """Returns whether what's inside this space is an organism."""
        return issubclass(type(self.contents), Protozoa)

    @return_false_if_boundary
    def contains_edible(self):
        # in the future, there will be more things to eat than other organisms
        return self.contains_organism()

    @return_false_if_boundary
    def contains_obstruction(self):
        return issubclass(type(self.contents), static_objects.Wall)

    @return_false_if_boundary
    def contains_drinkable(self):
        return issubclass(type(self.contents), static_objects.Water)


# TODO: make the world 3D, like dwarf fortress
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
        # TODO: Abstract grid into metadata class
        self.grid = [GridSpace() for i in range(self.width * self.height)]
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
        """Takes a step forwards in time.
        
        Returns the number of organisms currently alive."""
        living_organisms = 0
        for o in self.organisms.keys():
            o_x, o_y = self.organisms[o] % self.width, self.organisms[o] // self.width
            environment = get_cardinal_map(self.grid, o_x, o_y, self.width, self.height)
            move = o.move(environment)
            # TODO: attack, defend
            # TODO: refactor these actions into methods
            if move is Moves.FORWARD:
                self.relocate_by_direction(self.organisms[o], o.orientation)
            elif move is Moves.LEFT:
                self.rotate_organism(o, clockwise = False)
            elif move is Moves.RIGHT:
                self.rotate_organism(o)
            elif move is Moves.EAT:
                in_front = environment[o.orientation]
                if in_front.contains_organism():
                    other_o = in_front.contents
                    # TODO: damage can be dealt to more things than organisms
                    # TODO: eating does less damage than attacking
                    # Damage the creature we're eating
                    if o.strength > in_front.health:
                        other_o.health = 0
                    else:
                        other_o.health -= o.strength
                    # TODO: different creatures have different degrees of
                    #       metabolic efficiency
                    # TODO: depending on what they eat, they'll get more or
                    #       less nutrients out of it
                    # TODO: eating a live creature gives far less nutrients
                    # Regain calories and hydration from the creature we ate
                    o.calories += 5
                    o.hydration += 1
            elif move is Moves.DRINK:
                in_front = environment[o.orientation]
                if in_front.contains_drinkable():
                    # TODO: different creatures consume water more efficiently than others
                    # TODO: there are different amounts of water in a given area
                    o.hydration += 5

            if o.alive:
                living_organisms += 1
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
                space = self.grid[col + (row * self.width)]
                representation = ' '
                if space.contains_organism():
                    representation = str(space.contents)[0] # organism's representation char
                elif space.contains_drinkable():
                    representation = '~' # represent drinkable liquid
                elif space.contains_obstruction():
                    representation = '=' # represent impassable objects
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
        # TODO: this should also be a grid method
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
            if dest >= 0 and self.grid[dest].is_empty():
                # if this is an organism, keep track of its location
                if self.grid[index].contains_organism():
                    self.organisms[self.grid[index].contents] = dest
                self.grid[dest].move_from(self.grid[index])
                success = True
        except IndexError:
            pass

        return success

    def rotate_organism(self, organism, clockwise = True):
        """Changes the creature's cardinal orientation.

        Params:
            organism - a descendant of organisms.Protozoa to rotate
            clockwise - whether to turn the creature clockwise"""
        cur_dir = ORDER_OF_CARDINAL_DIRECTIONS.index(organism.orientation)
        rotate_dir = -1 if clockwise else 1
        new_dir = (cur_dir + rotate_dir) % len(ORDER_OF_CARDINAL_DIRECTIONS)
        organism.orientation = ORDER_OF_CARDINAL_DIRECTIONS[new_dir]

    def find_empty_space(self):
        """Locates an empty space on the grid."""
        # TODO: this should be moved to the grid object, when it exists
        increment = 1
        base_location = location = randint(0, len(self.grid) - 1)
        while not self.grid[location].is_empty():
            location = (base_location + increment**2) % len(self.grid)
            increment += 2

        return location

    def add_object(self, obj):
        """Places an object in an empty grid space."""
        location = self.find_empty_space()
        self.grid[location].put(obj)

    def add_organisms(self, organisms):
        """Adds each organism somewhere to the grid, and tracks that location."""
        for organism in organisms:
            location = self.find_empty_space()
            self.grid[location].put(organism)
            self.organisms[organism] = location
