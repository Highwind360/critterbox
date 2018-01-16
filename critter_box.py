#!/usr/bin/env python3
"""
critter_box.py
highwind

The CitterBox creates a world in which organisms are born,
survive, and take on their parents traits. It's an experiment performed to
play with the process of natural selection and the effects of imposing contrived
regulaions on a free market.
"""

from . import worlds
from . import organisms


def main():
    print("Beginning simulation...")
    # TODO: assign identifiers to organisms and ensure they are all unique
    orgs = [ organisms.Stagnator(i) for i in range(9) ]
    orgs.append(organisms.LoudWalker(10))
    world = worlds.BaseWorld(organisms = orgs)
    print("Sim started.")
    simulating = True
    i = 0 # debug
    while simulating:
        print("Round:", i); i += 1 # Debug
        living = world.step()
        simulating = living > 0
    print("Simulation complete.")


if __name__ == "__main__":
    main()
