#!/usr/bin/env python3
"""
critter_box.py
highwind

The CitterBox creates a world in which organisms are born,
survive, and take on their parents traits. It's an experiment performed to
play with the process of natural selection and the effects of imposing contrived
regulaions on a free market.
"""

import curses
from time import sleep

from . import worlds
from . import organisms


def get_unique_id():
    """Creates a new unique identifier for keeping track of organisms."""
    pass

def main(window):
    step_time = 0
    dis_type = "text"
    if window is not None:
        step_time = 0.25
        window.clear()
        window.nodelay(True)
        curses.curs_set(False)
        dis_type = "curses"

    # TODO: assign identifiers to organisms and ensure they are all unique
    orgs = [ organisms.Stagnator(i) for i in range(9) ]
    orgs.append(organisms.Walker(10))
    world = worlds.BaseWorld(organisms = orgs, display_type = dis_type,
        window = window, dimensions = (51, 31))

    simulating = True
    while simulating:
        living = world.step()
        world.show()
        sleep(step_time)
        simulating = living > 0

    # If we're operating in curses mode, wait to close the screen until asked
    if window is not None:
        window.nodelay(False)
        window.getch()
