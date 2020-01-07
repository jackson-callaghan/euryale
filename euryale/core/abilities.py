"""Handle all information relative to abilities.

Split off for organization largely.
"""
import math
import json


class Abilities:
    """Class handling abilities.

    Mostly methods to get more useful information from stored values.
    """

    def __init__(self, cdata):
        """Instantiate the Abilities class.

        Args:
            cdata (dict): character data
        """
        with open("data/abilities.json", "r") as ability_map_file:
            self.ability_map = json.load(ability_map_file)
        """TODO convert all these to underscore storage values,
        and create properties for all of them.
        """
        self._str = cdata.get("abilities").get("strength")
        self._dex = cdata.get("abilities").get("dexterity")
        self._con = cdata.get("abilities").get("constitution")
        self._int = cdata.get("abilities").get("intelligence")
        self._wis = cdata.get("abilities").get("wisdom")
        self._cha = cdata.get("abilities").get("charisma")

    @property
    def str(self):
        """Get the strength score. Set the strength score.

        Returns:
            int: see above.

        """
        return self._str

    @str.setter
    def str(self, value):
        self._str = value

    @property
    def dex(self):
        """Get the dexterity score. Set the dexterity score.

        Returns:
            int: see above.

        """
        return self._dex

    @dex.setter
    def dex(self, value):
        self._dex = value

    @property
    def con(self):
        """Get the constitution score. Set the constitution score.

        Returns:
            int: see above.

        """
        return self._con

    @con.setter
    def con(self, value):
        self._con = value

    @property
    def int(self):
        """Get the intelligence score. Set the intelligence score.

        Returns:
            int: see above.

        """
        return self._int

    @int.setter
    def int(self, value):
        self._int = value

    @property
    def wis(self):
        """Get the wisdom score. Set the wisdom score.

        Returns:
            int: see above.

        """
        return self._wis

    @wis.setter
    def wis(self, value):
        self._wis = value

    @property
    def cha(self):
        """Get the charisma score. Set the charisma score.

        Returns:
            int: see above.

        """
        return self._cha

    @cha.setter
    def cha(self, value):
        self._cha = value

    @property
    def abilities(self):
        """Return a dict of all ability scores.

        Returns:
            dict: see above.

        """
        skills = {}
        skills["str"] = self.str
        skills["dex"] = self.dex
        skills["con"] = self.con
        skills["int"] = self.int
        skills["wis"] = self.wis
        skills["cha"] = self.cha

        return skills

    @property
    def str_mod(self):
        """Return the strength modifier.

        Returns:
            int: Strength modifier based on strength score.

        """
        return math.floor((self.str - 10) / 2)

    @property
    def dex_mod(self):
        """Return the dexterity modifier.

        Returns:
            int: dexterity modifier based on dexterity score.

        """
        return math.floor((self.dex - 10) / 2)

    @property
    def con_mod(self):
        """Return the constitution modifier.

        Returns:
            int: constitution modifier based on constitution score.

        """
        return math.floor((self.con - 10) / 2)

    @property
    def int_mod(self):
        """Return the intelligence modifier.

        Returns:
            int: intelligence modifier based on intelligence score.

        """
        return math.floor((self.int - 10) / 2)

    @property
    def wis_mod(self):
        """Return the wisdom modifier.

        Returns:
            int: wisdom modifier based on wisdom score.

        """
        return math.floor((self.wis - 10) / 2)

    @property
    def cha_mod(self):
        """Return the charisma modifier.

        Returns:
            int: charisma modifier based on charisma score.

        """
        return math.floor((self.cha - 10) / 2)

    @property
    def modifiers(self):
        """Return a dictionary of all modifiers.

        Returns:
            dict: see above.

        """
        mod = {}
        mod["str"] = self.str_mod
        mod["dex"] = self.dex_mod
        mod["con"] = self.con_mod
        mod["int"] = self.int_mod
        mod["wis"] = self.wis_mod
        mod["cha"] = self.cha_mod

        return mod

    def skill_mod(self, skill):
        """Return a given skill modifier by name.

        Args:
            ability (str): ability short name

        Returns:
            int: skill mod

        """
        mod = 0
        for ab, sk in self.ability_map.items():
            if skill in sk:
                mod += self.modifiers[ab]
        return mod
