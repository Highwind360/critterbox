"""
organisms.py
highwind

Organisms for the sim, such as food and regular creatures.
"""

from .constants import Moves


class Protozoa():
    """An unintelligent organism: the blueprint for derivative organisms.

    It needs water and food to survive. With each tick, it consumes one point of
    hydration. Each time it makes a movement, such as rotating, it also
    consumes a calorie. Note that eating requires two calories.
    
    Params:
        ident - a hex word identifying the organism
        alive - whether the creature is spawned living, default True
        orientation - cardinal direction to face when spawned,
            is random if not provided"""

    calories = 0
    hydration = 0
    default_move = Moves.WAIT
    # TODO:
    #   eat/drink
    #   shelter
    #   reproduce

    def __init__(self, ident, alive = True, orientation = None):
        self.orientation = orientation
        self.alive = alive
        if type(ident) is not int or ident < 0 or ident > 0xffffffff:
            raise ValueError("Parameter 'ident' should be a hex word." + \
                             " Instead got: {}".format(ident))
        self.organism_identifier = ident

    @property
    def name(self):
        """Returns the classname with id appended, as a string."""
        return "".format(self.__class__.__name__, self.organism_identifier)

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

    # TODO: rotate 90 method


class Stagnator(Protozoa):
    """An orgasm that sits in a stationary location until it dies."""
    hydration = 10

class LoudWalker(Protozoa):
    """An organism that walks straight and announces each time it does so."""
    hydration = 20
    calories = 10

    def think(self, info):
        print(info)
        print("I'm facing {}. There is a {} in front of me".format(
            self.orientation, info[self.orientation]))
        return Moves.FORWARD
