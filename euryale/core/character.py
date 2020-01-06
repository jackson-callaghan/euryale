"""character.py

Contains the Character class, which manages information storage during runtime.
"""

import json
import math
from . import inventory
from . import magic
from . import notes


class Character:
    """Character class."""

    def __init__(self, cdata):

        # load class list for later use (calculations)
        with open("data/classes.json", "r") as classes_file:
            self.class_list = json.load(classes_file)
        with open("data/abilities.json", "r") as ability_map_file:
            self.ability_map = json.load(ability_map_file)

        # ---- "incalculable" values ----

        self.name = cdata.get("name")
        self.race = cdata.get("race")
        self.subrace = cdata.get("subrace")
        self.size = cdata.get("size")
        self.speed = cdata.get("speed")
        self.gender = cdata.get("gender")
        self.age = cdata.get("age")
        self.height = cdata.get("height")
        self.weight = cdata.get("weight")
        self.skin = cdata.get("skin")
        self.eyes = cdata.get("eyes")
        self.hair = cdata.get("hair")
        self.character_level = cdata.get("level")
        self.starting_class = cdata.get("starting class")
        # dict of class: level (first class must be len 1 list)
        self.classes = cdata.get("classes")
        # dict of class: subclass
        self.subclass = cdata.get("subclass")

        # holds either rolled health or None to indicate auto-health calc
        self._max_health = cdata.get("max health")
        self.health = cdata.get("health")
        self.temp_health = 0
        self.background = cdata.get("background")
        self.religion = cdata.get("religion")

        self.abilities = cdata.get("abilities")
        self.strength = cdata.get("abilities").get("strength")
        self.dexterity = cdata.get("abilities").get("dexterity")
        self.constitution = cdata.get("abilities").get("constitution")
        self.intelligence = cdata.get("abilities").get("intelligence")
        self.wisdom = cdata.get("abilities").get("wisdom")
        self.charisma = cdata.get("abilities").get("charisma")

        self.proficiencies = cdata.get("proficiencies")
        self.languages = cdata.get("languages")
        self.feats = cdata.get("feats")
        self.inventory = cdata.get("inventory")
        self.max_attuned = cdata.get("max_attuned")
        self.attuned = cdata.get("attuned")
        self.notes = cdata.get("notes")
        self.spells_known = cdata.get("spells known")
        self._spells_prepared = cdata.get("spells prepared")
        self._spell_slots = cdata.get("spell slots")

        self.dice = {
            "2": [i for i in range(1, 3)],
            "4": [i for i in range(1, 5)],
            "6": [i for i in range(1, 7)],
            "8": [i for i in range(1, 9)],
            "10": [i for i in range(1, 11)],
            "12": [i for i in range(1, 13)],
            "20": [i for i in range(1, 21)],
            "100": [i for i in range(1, 101)]
        }

    def __str__(self):
        line1 = "{}: {} {} {}. {}. \n".format(
            self.name,
            self.size,
            self.subrace,
            self.race,
            self.gender
        )
        line2 = ", ".join(
            ["level {} {} {}".format(
                self.classes[i],
                self.subclass[i],
                i
            )
                for i in self.classes.keys()],

        )

        line3 = "\n".join((
            str(self.strength),
            str(self.dexterity),
            str(self.constitution),
            str(self.intelligence),
            str(self.wisdom),
            str(self.charisma)
        ))

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
                    total += diepair[0] + self.constitution_mod
                    total += ((diepair[0] / 2) + 1 +
                              self.constitution_mod) * (diepair[1] - 1)
                else:
                    total += (diepair[0] / 2) + 1 + \
                        self.constitution_mod * diepair[1]

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
    def strength_mod(self):
        """Return the strength modifier.

        Returns:
            int: Strength modifier based on strength score.

        """
        return math.floor((self.strength - 10) / 2)

    @property
    def dexterity_mod(self):
        """Return the dexterity modifier.

        Returns:
            int: dexterity modifier based on dexterity score.

        """
        return math.floor((self.dexterity - 10) / 2)

    @property
    def constitution_mod(self):
        """Return the constitution modifier.

        Returns:
            int: constitution modifier based on constitution score.

        """
        return math.floor((self.constitution - 10) / 2)

    @property
    def intelligence_mod(self):
        """Return the intelligence modifier.

        Returns:
            int: intelligence modifier based on intelligence score.

        """
        return math.floor((self.intelligence - 10) / 2)

    @property
    def wisdom_mod(self):
        """Return the wisdom modifier.

        Returns:
            int: wisdom modifier based on wisdom score.

        """
        return math.floor((self.wisdom - 10) / 2)

    @property
    def charisma_mod(self):
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

    @property
    def n_attuned(self):

        return len(self.attuned)

    @property
    def inventory_names(self):

        return [i for i in self.inventory.keys()]

    @property
    def spells_prepared(self):
        if "0" in self._spells_prepared.keys():
            return self._spells_prepared
        else:
            self._spells_prepared["0"] = self.spells_known["0"]
            return self._spells_prepared

    @spells_prepared.setter
    def spells_prepared(self, value):
        self._spells_prepared = value

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

    def ability_mod(self, ability):
        mod = 0
        for sk, ab in self.ability_map.items():
            if ability in ab:
                mod += self.modifiers[sk]
        return mod

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
        if dtype is not None:
            for feat in self.feats:
                if feat["category"] == "passive":
                    # TODO change modifies accessor to proper structure
                    if (feat["type"] == "vulnerability"
                            and feat["modifies"] == dtype):
                        value = math.floor(value * 2)
                    if (feat["type"] == "resistance"
                            and feat["modifies"] == dtype):
                        value = math.floor(value / 2)

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
