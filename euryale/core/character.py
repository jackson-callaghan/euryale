"""Character class.

Contains character information and references to other information storage
for things such as inventory and spells. Effectively the central control for
a loaded character, to be used as an API of sorts for whatever interface loads
the character.

RULE: If it cannot be directly set, make it a function, instead of a property.
      If it can be directly set, make it a property.

TODO: ensure you've got getters/setters for basically everything
TODO: deside how the registry will work
TODO: write in basic logic for getting modifiers, see max_hp for example
TODO: using previous, make list of pre-defined modifiers
"""

import json
import math
from core import abilities as ab
from core import feats as ft
from core import inventory as iv
from core import magic as mg
from core import registry as rg


def standard_dialog(prompt):
    return input(prompt)


class Character:
    """Character class."""

    def __init__(self, cdata, outcb=print, dialogcb='default'):
        """Instantiate the character given its data.

        Args:
            cdata (dict): Dictionary of character data, from read_char
            outcb (func): Callback function for displaying information
            dialogcb (func): Callback function for when a dialog must be
                presented

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
        self.abilities = ab.Abilities(self, cdata)
        self.feats = ft.Feats(cdata)
        self.inventory = iv.Inventory(cdata)
        self.magic = mg.Magic(cdata)

        # ---- characteristics ----
        self.name = cdata.get("name", "Simpleton")
        self.race = cdata.get("race", "Simpleton")
        self.subrace = cdata.get("subrace", None)
        self.size = cdata.get("size", "Medium")
        self.speed = cdata.get("speed", 30)
        self.gender = cdata.get("gender", "?")
        self.age = cdata.get("age", 0)
        self.height = cdata.get("height", 0)
        self.weight = cdata.get("weight", 0)
        self.skin = cdata.get("skin", "Nondescript")
        self.eyes = cdata.get("eyes", "Nondescript")
        self.hair = cdata.get("hair", "Nondescript")
        self.background = cdata.get("background", None)
        self.alignment = cdata.get("alignment", None)
        self.religion = cdata.get("religion", None)

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
        self.subclasses = cdata.get("subclasses", None)

        # ---- some more information ----
        # holds either rolled hp or None to indicate auto-hp calc
        self._max_hp = cdata.get("max hp", None)
        self.hp = cdata.get("hp", self.max_hp)
        self.temp_hp = cdata.get("temp hp", 0)

        self.languages = cdata.get("languages", [])
        # dict of proficiency: level (1 for proficient, 2 for expertise)

        self._max_attuned = cdata.get("max_attuned", None)
        self._attuend = cdata.get("attuned", None)
        self._n_attuned = cdata.get("n_attuned", None)

        # registry of modifiers
        self.registry = rg.Registry(self)

        # register dialog callbacks
        self.outcb = outcb
        if dialogcb is None:
            self.dialogcb = standard_dialog
        else:
            self.dialogcb = dialogcb

    def __str__(self):
        """Return string format of character sheet.

        Minimal amount of information, really only useful for debug.

        Returns:
            str: see above.

        """
        # TODO: re-write this for useful at-a-glance info
        line1 = "{}: {} {} {}. {}.".format(
            self.name,
            self.size,
            self.subrace,
            self.race,
            self.gender)
        line2 = ", ".join(
            ["level {} {} {}".format(
                self.classes[i],
                self.subclasses[i],
                i)
                for i in self.classes.keys()])
        line3 = "\n".join("{:12} : {:2d}".format(ab, sc)
                          for ab, sc in self.abilities.abilities.items())

        return "\n".join((line1, line2, line3))

    @property
    def max_hp(self):
        """Return max hp.

        Returns:
            int: Max hp

        """
        mhp = 0
        if self._max_hp is not None:  # if it's custom set
            mhp = self._max_hp
        else:  # otherwise auto-calculate
            for class_, diepair in self.max_hit_dice().items():
                # diepair: 0: hitdie value, 1: number of hitdie
                if class_ == self.starting_class:
                    mhp += (diepair[0] +
                            self.abilities.ability_mod("constitution"))
                    mhp += ((diepair[0] / 2) +
                            1 +
                            (self.abilities.ability_mod("constitution")) *
                            (diepair[1] - 1))
                else:
                    mhp += (diepair[0] / 2) + 1 + \
                        self.abilities.ability_mod("constitution") * diepair[1]

        # if "max_hp" in self.registry

        return mhp  # return the final maximum hp calculation

    @max_hp.setter
    def max_hp(self, value):
        self._max_hp = value

    @property
    def max_attuned(self):
        return self._max_attuned

    @max_attuned.setter
    def max_attuned(self, value):
        self._max_attuned = value

    @property
    def attuned(self):
        return self._attuned

    @attuned.setter
    def attuned(self, value):
        self._attuned = value

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

    def n_attuned(self):
        """Return the number of attuned magic items.

        Returns:
            int: The number of attuned items.

        """
        return len(self.attuned)

    def is_multiclassed(self):
        """Check if character is multiclassed.

        Returns:
            bool: True if character is multiclassed else False

        """
        return True if len(self.classes) > 1 else False

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

    def mod_hp(self, value):
        """Modify current hp value.

        If healing above maximum, hp will be set to max. If taking damage
        greater than negative maximum, returns death signifier.

        Args:
            value (int): hp change, either negative or positive.

        Returns:
            int, str: new hp or death signifier.

        """
        if self.hp + value >= self.max_hp:
            self.hp = self.max_hp
        elif self.hp + value <= 0 - self.max_hp:
            self.hp += value
            return "death"
        else:
            self.hp += value
            return self.hp

    def heal(self, value):
        """Heal the given amount.

        Args:
            value (int): amount to healh.

        Returns:
            int: amount healed.

        """
        self.mod_hp(value)

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

        self.mod_hp(-value)

        return value


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
