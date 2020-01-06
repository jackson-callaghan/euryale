"""Various utility methods.

All of them are small enough that I didn't really care to put them in their own
files.
"""

import json

DICE = {
    "2": [i for i in range(1, 3)],
    "4": [i for i in range(1, 5)],
    "6": [i for i in range(1, 7)],
    "8": [i for i in range(1, 9)],
    "10": [i for i in range(1, 11)],
    "12": [i for i in range(1, 13)],
    "20": [i for i in range(1, 21)],
    "100": [i for i in range(1, 101)]
}


def read_char(name):

    with open("data/characters/{}.json".format(name), "r") as character_file:
        cdata = json.load(character_file)

    return cdata
