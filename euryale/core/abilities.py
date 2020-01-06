import math


class Abilities():

    def __init__(self, cdata):
        self.abilities = cdata.get("abilities")
        self.str = cdata.get("abilities").get("strength")
        self.dex = cdata.get("abilities").get("dexterity")
        self.con = cdata.get("abilities").get("constitution")
        self.int = cdata.get("abilities").get("intelligence")
        self.wis = cdata.get("abilities").get("wisdom")
        self.cha = cdata.get("abilities").get("charisma")

    @property
    def str_mod(self):
        """Return the strength modifier.

        Returns:
            int: Strength modifier based on strength score.

        """
        return math.floor((self.strength - 10) / 2)

    @property
    def dex_mod(self):
        """Return the dexterity modifier.

        Returns:
            int: dexterity modifier based on dexterity score.

        """
        return math.floor((self.dexterity - 10) / 2)

    @property
    def con_mod(self):
        """Return the constitution modifier.

        Returns:
            int: constitution modifier based on constitution score.

        """
        return math.floor((self.constitution - 10) / 2)

    @property
    def int_mod(self):
        """Return the intelligence modifier.

        Returns:
            int: intelligence modifier based on intelligence score.

        """
        return math.floor((self.intelligence - 10) / 2)

    @property
    def wis_mod(self):
        """Return the wisdom modifier.

        Returns:
            int: wisdom modifier based on wisdom score.

        """
        return math.floor((self.wisdom - 10) / 2)

    @property
    def cha_mod(self):
        """Return the charisma modifier.

        Returns:
            int: charisma modifier based on charisma score.

        """
        return math.floor((self.charisma - 10) / 2)

    @property
    def modifiers(self):
        mod = {}
        mod["strength"] = self.strength_mod
        mod["dexterity"] = self.dexterity_mod
        mod["constitution"] = self.constitution_mod
        mod["intelligence"] = self.intelligence_mod
        mod["wisdom"] = self.wisdom_mod
        mod["charisma"] = self.charisma_mod

        return mod

    def ability_mod(self, ability):
        mod = 0
        for sk, ab in self.ability_map.items():
            if ability in ab:
                mod += self.modifiers[sk]
        return mod
