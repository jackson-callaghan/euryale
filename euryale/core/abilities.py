"""Handle all information relative to abilities.

Split off for organization largely.
"""
import math
import json


class Abilities:
    """Class handling abilities.

    Mostly methods to get more useful information from stored values.
    """

    def __init__(self, parent, cdata):
        """Instantiate the Abilities class.

        Args:
            cdata (dict): character data
        """
        self.parent = parent
        self.abilities = cdata.get("abilities", None)
        for ab in self.parent.ability_map.keys():
            if ab not in self.abilities.keys():
                self.abilities[ab] = 0
        self.proficiencies = cdata.get("proficiencies", {})

    def get_abilities(self):
        """Return a dict of all ability scores.

        Returns:
            dict: see above.

        """
        for ab in self.parent.ability_map.keys():
            if ab not in self.abilities.keys():
                self.abilities[ab] = 0
        abilities = {}
        for ab, score in self.abilities.items():
            abilities[ab] = score

        return abilities

    def ability_modifiers(self):
        """Return a dictionary of all modifiers.

        Returns:
            dict: see above.

        """
        mod = {}
        for ab, score in self.get_abilities().items():
            mod[ab] = math.floor((score - 10) / 2)

        return mod

    def ability(self, ability):
        return self.get_abilities()[ability]

    def ability_mod(self, ability):
        return self.ability_modifiers()[ability]

    def skill_mod(self, skill):
        """Return a given skill modifier by name.

        Args:
            ability (str): ability short name

        Returns:
            int: skill mod

        """
        mod = 0
        for ab, sk in self.parent.ability_map.items():
            if skill in sk:
                mod += self.ability_modifiers()[ab]
        if self.has_proficiency(skill):
            mod += self.proficiency_bonus()
        return mod

    def has_proficiency(self, proficiency):
        """Check if character has a proficiency.

        Args:
            proficiency (str): name of a proficiency

        Returns:
            int: proficiency level (1 for proficiency, 2 for expertise) or 0

        """
        if proficiency in self.proficiencies.keys():
            return self.proficiencies[proficiency]
        else:
            return 0

    def proficiency_bonus(self):
        """Return the current proficiency bonus.

        Returns:
            int: Proficiency bonus based on level.

        """
        return math.ceil((self.parent.character_level / 4) + 1)
