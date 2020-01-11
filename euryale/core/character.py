"""Character class.

Contains character information and references to other information storage
for things such as inventory and spells. Effectively the central control for
a loaded character, to be used as an API of sorts for whatever interface loads
the character.

TODO: add support for display versions of all calculated values as a stop-gap
"""

import json
import math
from core import abilities as ab
from core import feats as ft
from core import inventory as iv
from core import magic as mg


class Character:
    """Character class."""

    def __init__(self, cdata):
        """Instantiate the character given its data.

        Args:
            cdata (dict): Dictionary of character data, from read_char

        Raises:
            ValueError: If character has no starting class.
            ValueError: If character has no class.

        """
        # load class list for later use (calculations)
        with open("data/classes.json", "r") as classes_file:
            self.class_list = json.load(classes_file)
        with open("data/abilities.json", "r") as ability_map_file:
            self.ability_map = json.load(ability_map_file)

        # ---- Info stored in special classes ----
        self.abilities = ab.Abilities(cdata)
        self.feats = ft.Feats(cdata)
        self.inventory = iv.Inventory(cdata)
        self.magic = mg.Magic(cdata)

        # ---- characteristics ----
        self.name = cdata.get("name", "Simpleton")
        self.race = cdata.get("race", "Simpleton")
        self.subrace = cdata.get("subrace", None)
        self.size = cdata.get("size", "Medium")
        self.speed = cdata.get("speed", 30)
        self.gender = cdata.get("gender", "NB")
        self.age = cdata.get("age", 0)
        self.height = cdata.get("height", 0)
        self.weight = cdata.get("weight", 0)
        self.skin = cdata.get("skin", "Nondescript")
        self.eyes = cdata.get("eyes", "Nondescript")
        self.hair = cdata.get("hair", "Nondescript")

        # ---- level/class information ----
        self.character_level = cdata.get("level", 1)

        self.starting_class = cdata.get("starting class", None)
        if self.starting_class is None:
            raise ValueError("character starting class must be defined!")

        # dict of class: level (first class must be len 1 list)
        self.classes = cdata.get("classes", None)
        if self.classes is None:
            raise ValueError("missing class level dictionary!")

        # dict of class: subclass
        self.subclass = cdata.get("subclass", None)

        # ---- some more information ----
        # holds either rolled health or None to indicate auto-health calc
        self._max_health = cdata.get("max health", None)
        self.health = cdata.get("health", self.max_health)
        self.temp_health = cdata.get("temp health", 0)
        self.background = cdata.get("background", None)
        self.religion = cdata.get("religion", None)
        # dict of proficiency: level (1 for proficient, 2 for expertise)
        self.proficiencies = cdata.get("proficiencies", {})
        self.languages = cdata.get("languages", [])

    def __str__(self):
        """Return string format of character sheet.

        Minimal amount of information, really only useful for debug.

        Returns:
            str: see above.

        """
        line1 = "{}: {} {} {}. {}. \n".format(
            self.name,
            self.size,
            self.subrace,
            self.race,
            self.gender)
        line2 = ", ".join(
            ["level {} {} {}".format(
                self.classes[i],
                self.subclass[i],
                i)
                for i in self.classes.keys()])
        line3 = "\n".join((
            str(self.abilities.str),
            str(self.abilities.dex),
            str(self.abilities.con),
            str(self.abilities.int),
            str(self.abilities.wis),
            str(self.abilities.cha)))

        return "\n".join((line1, line2, line3))

    @property
    def max_hit_dice(self):
        """Return max hit dice.

        Returns:
            dict: Max hit dice.

        """
        max_hit_dice = {}
        for class_, level in self.classes.items():
            # diepair: 0: hitdie value, 1: number of hitdie from class levels
            max_hit_dice[class_] = (self.class_list[class_]["hit die"], level)
        return max_hit_dice

    @property
    def max_health(self):
        """Return max health.

        Returns:
            int: Max health

        """
        if self._max_health is not None:
            return self._max_health
        else:
            total = 0
            for class_, diepair in self.max_hit_dice.items():
                # diepair: 0: hitdie value, 1: number of hitdie
                if class_ == self.starting_class:
                    total += diepair[0] + self.abilities.con_mod
                    total += ((diepair[0] / 2) + 1 +
                              self.abilities.con_mod) * (diepair[1] - 1)
                else:
                    total += (diepair[0] / 2) + 1 + \
                        self.abilities.con_mod * diepair[1]

            return total

    @max_health.setter
    def max_health(self, value):
        self._max_health = value

    @property
    def proficiency_bonus(self):
        """Return the current proficiency bonus.

        Returns:
            int: Proficiency bonus based on level.

        """
        return math.ceil((self.character_level / 4) + 1)

    @property
    def n_attuned(self):
        """Return the number of attuned magic items.

        Returns:
            int: The number of attuned items.

        """
        return len(self.attuned)

    def update_classes(self, **kwargs):
        """Replace current classes and levels.

        Args:
            **kwargs (int): class=level

        """
        self.classes = {}
        for class_, lvl in kwargs.items():
            if class_ not in self.class_list.keys():
                raise ValueError("class does not exist")
            if isinstance(self.classes[class_], list):
                self.classes[class_][0] = lvl
            else:
                self.classes[class_] = lvl
        # TODO add update calls for everything that is updated based on class
        """things to update:
        - idk yet
        """

    @property
    def is_multiclassed(self):
        """Check if character is multiclassed.

        Returns:
            bool: True if character is multiclassed else False

        """
        return True if len(self.classes) > 1 else False

    def level_up(self, clas):
        """Level up a given class.

        Args:
            clas (str): Class name.

        Raises:
            ValueError: If class is not in classes.json.

        """
        clevels = self.classes

        if clas not in self.class_list.keys():
            raise ValueError("class does not exist")

        if clas not in self.classes.keys():
            clevels[clas] = 1
        else:
            clevels[clas] += 1

        self.character_level += 1
        self.update_classes(**clevels)

    def mod_health(self, value):
        """Modify current health value.

        If healing above maximum, health will be set to max. If taking damage
        greater than negative maximum, returns death signifier.

        Args:
            value (int): Health change, either negative or positive.

        Returns:
            int, str: new health or death signifier.

        """
        if self.health + value >= self.max_health:
            self.health = self.max_health
        elif self.health + value <= 0 - self.max_health:
            self.health += value
            return "death"
        else:
            self.health += value
            return self.health

    def heal(self, value):
        """Heal the given amount.

        Args:
            value (int): amount to healh.

        Returns:
            int: amount healed.

        """
        self.mod_health(value)

        return value

    def take_damage(self, value, dtype=None):
        """Take a given amount of damage.

        Takes into account resistance and vulnerability if given type.

        Args:
            value (int): Amount of damage
            type_ (str): Type of damage. Defaults to None.

        Returns:
            int: Final damage taken.

        """
        # if dtype is not None:
        #     for feat in self.feats:
        #         if feat["category"] == "passive":
        #             # TODO change modifies accessor to proper structure
        #             if (feat["type"] == "vulnerability"
        #                     and feat["modifies"] == dtype):
        #                 value = math.floor(value * 2)
        #             if (feat["type"] == "resistance"
        #                     and feat["modifies"] == dtype):
        #                 value = math.floor(value / 2)

        self.mod_health(-value)

        return value

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

# TODO make own files for inventory, spells, feats, notes
    # classes to manage each, so access would be like char.inventory.add
    # and suchlike
# TODO add attributes and properties to access all information in class json
    # spell slots
    # max spells prepared
# TODO figure out proper (prefereable extensible) format for feats/inventory
    # flags with program-handled defaults? for instance attunement flag, which
    # defaults to False if it's not found
# TODO docstring everything and reformat to be easier to read
