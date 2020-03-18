"""Maintains a dictionary of modifiers on any given thing.

Can be passive, on specified trigger. On use is handled by the item itself,
but may add temporary modifiers to the registry. Registry lookup is done by
any method that handles numbers, and should expect to lookup using roughly its
own name.
"""

from dice_notation.parser import DiceParser

# TODO implement registry items


class RegItem:
    """Registry Item.

    Contains all the information required for modifiers, etc.
    """

    def __init__(self, parent, data):
        """Initialize a registry item.

        Args:
            name (str): the name of the registry item.
        """
        self.name = data.get("name")
        self.description = data.get("description")
        self.parent = parent
        self.activation = data.get("activation")
        self.charges = data.get("charges")
        self.chperuse = data.get("charges per use")
        self.used = data.get("used")
        self.duration = data.get("duration")
        self.active = data.get("active")
        self.recoverywhen = data.get("recoverywhen")
        self.recoveryamt = data.get("recoveryamt")
        self.modlist = data.get("modlist")
        self.modtype = data.get("modtype")
        self.mod = data.get("mod")

    # TODO self handling method given number
    def handle(n):
        if self.activation == "passive":

            # TODO implement registry


class Registry:
    """Registry.

    Contains all the registry items, and methods for interfacing with them.
    """

    def __init__(self):
        None
