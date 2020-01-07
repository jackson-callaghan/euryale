"""Maintains a dictionary of modifiers on any given thing.

Can be passive, on specified trigger. On use is handled by the item itself,
but may add temporary modifiers to the registry. Registry lookup is done by
any method that handles numbers, and should expect to lookup using roughly its
own name.
"""


class Registry:
    """Registry Class.

    Mostly holds methods for registry editing.
    """

    def __init__(self):
        """Instantiate the Registry class.

        Does not read in the registry, another method must be called for this.
        """
        self.reg = {}

    def additem(self, item):
        """Add an item to the registry.

        Args:
            item (dict): dictionary of selector: str, and data: dict
        """
        selector = item.get("selector")
        data = item.get("data")
        self.reg[selector] = data

    def removeitem(self, selector):
        """Remove an item from the registry.

        Args:
            selector (str): selector
        """
        self.reg.pop(selector)
