"""Various utility methods.

All of them are small enough that I didn't really care to put them in their own
files.
"""

import json


def read_char(name):

    with open("data/characters/{}.json".format(name), "r") as character_file:
        cdata = json.load(character_file)

    return cdata
