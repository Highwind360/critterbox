"""
organisms.py
highwind

Organisms for the sim, such as food and regular creatures.
"""

from .constants import Moves, Directions


class Protozoa():
    """An unintelligent organism: the blueprint for derivative organisms.

    It needs water and food to survive. With each tick, it consumes one point of
    hydration. Each time it makes a movement, such as rotating, it also
    consumes a calorie.
    
    Params:
        ident - a hex word identifying the organism
        alive - whether the creature is spawned living, default True
        orientation - cardinal direction to face when spawned,
            is random if not provided"""

    symbol = 'P'
    calories = 0
    hydration = 0
    max_health = 1
    strength = 1 # the amount of damage it does
    default_move = Moves.WAIT
    # TODO:
    #   Should eating/fighting take more calories?
    #   reproduce
    #   shelter
    #       Being in too cold a weather will burn calories (to stay warm)
    #       Being in too hot a weather will burn extra hydration

    def __init__(self, ident, alive = True, orientation = Directions.NORTH):
        self.orientation = orientation
        self.alive = alive
        if type(ident) is not int or ident < 0 or ident > 0xffffffff:
            raise ValueError("Parameter 'ident' should be a hex word." + \
                             " Instead got: {}".format(ident))
        self.organism_identifier = ident
        self.current_health = self.max_health

    def __str__(self):
        """Returns the representation of the organism."""
        return self.symbol

    @property
    def name(self):
        """Returns the classname with id appended, as a string."""
        return "{}#{}".format(self.__class__.__name__, self.organism_identifier)

    def think(self, info):
        """The important logic for an organism's decision making goes here.
        
        Params:
            info - a dict containing keys "Directions.{NORTH,SOUTH,EAST,WEST}",
            with the value for each entry being what's located in the
            environment at that location."""
        return self.default_move

    def age(self, move):
        """Processes all the things that happen to a creature's body during a
        regular time cycle."""
        if move in [Moves.LEFT, Moves.RIGHT, Moves.FORWARD, Moves.EAT]:
            self.calories -= 1 # calories to move
        self.hydration -= 1 # hydration to simply exist

    def move(self, environment):
        """Exerts the pressure of existing on a single organism, returning the
        decision that creature made."""
        move = self.think(environment)
        self.age(move)

        # have we died?
        if self.hydration < 0 or self.calories < 0:
            self.alive = False
            move = Moves.DEAD
        return move

    def rotate(self, clockwise = True):
        """Changes the creature's cardinal orientation."""
        cur_dir = ORDER_OF_CARDINAL_DIRECTIONS.index(self.orientation)
        rotate_dir = -1 if clockwise else 1
        new_dir = (cur_dir + rotate_dir) % len(ORDER_OF_CARDINAL_DIRECTIONS)
        self.orientation = ORDER_OF_CARDINAL_DIRECTIONS[new_dir]


class Stagnator(Protozoa):
    """An orgasm that sits in a stationary location until it dies."""
    symbol = 'S'
    hydration = 10


class Walker(Protozoa):
    """An organism that walks straight in a line."""
    symbol = 'W'
    calories = 10
    hydration = 20
    default_move = Moves.FORWARD
