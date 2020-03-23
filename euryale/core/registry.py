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

    def __init__(self, registry, parent, data):
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
        self.parser = DiceParser()

    # TODO self handling method given number
    def modify(self, n):

        # TODO add checking for currently active
        # TODO change this to work for non-printing interfaces
        if self.used is not None and self.charges is not None:
            if self.used >= self.charges:
                print("out of charges!")
                return False
                # TODO add attribute for word to use (charges/used/etc)
                # TODO figure out what to return

        # activation options
        if self.activation == "passive":  # modifier happens passively
            None  # not currently used for anything
        elif self.activation == "active":  # mod never activates on its own
            None  # not currently used for anything
        elif self.activation == "reactive":  # mod is passive, but optional
            print("")  # TODO print reminder and ask to use or not
            # TODO needs some sort of callback function for this
            # actually consider how you want to handle this so it works
            # for multiple interfaces and isn't a pain to deal with
        elif self.activation == "reminder":  # print desc for whatever reason
            print(self.description)  # for now just this
            # TODO change this to handle non-printing interfaces
        else:
            raise ValueError("unexpected activation value")

        # charges and duration
        if self.used is not None and self.charges is not None:
            self.used += self.chperuse
        if self.duration is not None:
            self.active = True

        # return modification
        if self.modtype == "delta":
            return n + self.parser.parse(self.mod).roll()
        elif self.modtype == "mult":
            return n * self.parser.parse(self.mod).roll()
        elif self.modtype == "div":
            return n / self.parser.parse(self.mod).roll()
        elif self.modtype == "min":
            return self.mod if n < self.mod else n
        elif self.modtype == "max":
            return self.mod if n > self.mod else n


# TODO implement registry
class Registry:
    """Registry.

    Contains all the registry items, and methods for interfacing with them.
    """

    def __init__(self, parent):
        None
