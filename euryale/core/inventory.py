"""Inventory management.

Mostly methods.
"""

# TODO add item class and requisite methods for inventory items to be useful.
# TODO convert current methods to use items


class Inventory:
    """Inventory class.

    Hold data in dict, and retrieves most things via methods.
    """

    def __init__(self, cdata):
        """Instantiate the inventory class.

        Args:
            cdata (dict): character data, from read_char.
        """
        self.inventory = cdata.get("inventory", {})

    @property
    def inventory_names(self):
        """Get a list of all inventory names.

        Returns:
            list: see above.

        """
        return [i for i in self.inventory.keys()]

    @property
    def attuned(self):
        """Return the currently attuned items.

        Returns:
            dict: see above.

        """
        att = {}
        for item, data in self.inventory.items():
            if data["attuned"] is True:
                att[item] = data
        return att

    @property
    def n_attuned(self):
        """Return the number of currently attuned items.

        Returns:
            dict: see above.

        """
        att = 0
        for item, data in self.inventory.items():
            if data["attuned"] is True:
                att += 1
        return att
