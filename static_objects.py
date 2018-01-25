"""
static_objects.py
highwind

A collection of objects that exist in the critterbox but don't move.
"""


class CritterBoxObject():
    pass


# TODO: water flows downhill
class Water(CritterBoxObject):
    """An object representing a pool of water.

    Params:
        depth - how deep the water in the square is"""

    def __init__(self, depth = 10):
        self.depth = depth


class Wall(CritterBoxObject):
    """An impassible barrier.

    Params:
        integrity - how sturdy the wall is
        thickness - the amount of digging it'll take to break down"""

    def __init__(self, integrity = 10, thickness = 10):
        if thickness < 0 or integrity < 0:
            raise ValueError("The wall's thickness and integrity must be positive.")
        elif thickness > 10 or integrity > 10:
            raise ValueError("10 is the max score for thickness and integrity.")
        self.thickness = thickness
        self.integrity = integrity
