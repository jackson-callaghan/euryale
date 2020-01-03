"""character.py

Contains the Character class, which manages information storage during runtime.
"""

import json
import math


class Character:
    """Character class."""

    def __init__(self, cdata):

        # "incalculable" values
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
        # dict of class: level (first class must be len 1 list)
        self.classes = cdata.get("classes")
        # dict of class: subclass
        self.subclass = cdata.get("subclass")
        # holds either rolled health or False to indicate auto-health calc

        #fix kwargs -> cdata etc
        self._max_health = kwargs.get("max health")
        self.background = kwargs.get("background")
        self.religion = kwargs.get("religion")

        self.strength = kwargs.get("abilities").get("strength")
        self.dexterity = kwargs.get("abilities").get("dexterity")
        self.constitution = kwargs.get("abilities").get("constitution")
        self.intelligence = kwargs.get("abilities").get("intelligence")
        self.wisdom = kwargs.get("abilities").get("wisdom")
        self.charisma = kwargs.get("abilities").get("charisma")

        self.proficiencies = kwargs.get("proficiencies")
        self.expertise = kwargs.get("expertise")
        self.languages = kwargs.get("languages")
        self.feats = kwargs.get("feats")
        self.inventory = kwargs.get("inventory")

        with open("../data/classes.json", "r") as classes_file:
            self.class_list = json.load(classes_file)

        # basic calculable values which should be updated manually
        self.dice = {
            "2": [i for i in range(1, 3)],
            "4": [i for i in range(1, 5)],
            "6": [i for i in range(1, 7)],
            "8": [i for i in range(1, 9)],
            "10": [i for i in range(1, 11)],
            "12": [i for i in range(1, 13)],
            "20": [i for i in range(1, 21)],
            "101": [i for i in range(1, 101)]
        }
        self.hit_dice = self.max_hit_dice
        self.health = self.max_health
        self.temp_health = 0

    @property
    def max_hit_dice(self):
        """Return max hit dice.

        Returns:
            dict: Max hit dice.

        """
        max_hit_dice = {}
        for class_, level in self.classes.items():
            max_hit_dice[str(self.class_list[class_]["hit die"])] = level
        return max_hit_dice

    @property
    def max_health(self):
        """Return max health.

        Returns:
            int: Max health

        """
        if self._max_health is not False:
            return self._max_health
        else:
            total = 0
            for die, lvl in self.max_hit_dice.items():
                total += (((int(die) / 2)+1) + self.constitution_mod) * lvl
                # apparently trying to multiply sequence and float?
            for class_, lvl in self.classes.items():
                if isinstance(lvl, list):
                    total += (int(self.class_list[class_]["hit die"]) / 2) - 1
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
    def inventory_names(self):
        return [i.name for i in self.inventory]

    def update_classes(self, **kwargs):
        """Replace current classes and levels.

        Args:
            **kwargs (int): class=level

        """
        self.classes = {}
        for c, l in kwargs.items():
            if c not in self.class_list.keys():
                raise ValueError("class does not exist")
            if isinstance(self.classes[c], list):
                self.classes[c][0] = l
            else:
                self.classes[c] = l
        # TODO add update calls for everything that is updated based on class
        """things to update:
        - idk yet
        """

    # def modify(self, value, modifiers):
    #     for modifier in modifiers:
    #         if modifier["type"] == "flat_delta":
    #             value += modifier["delta"]
    #         elif modifier["type"] == "multiplier":
    #             value *= modifier["delta"]
    #         elif modifier["type"] == "divider":
    #             value /= modifier["delta"]
    #         elif modifier["type"] == "dice_delta":
    #             reg = re.compile("(d)")
    #             delta = re.split(reg, modifier["delta"])
    #             if delta[0][0] == "-":
    #                 for i in range(int(delta[0][1:])):
    #                     value -= random.choice(self.dice[delta[2]])
    #             else:
    #                 for i in range(int(delta[0])):
    #                     value += random.choice(self.dice[delta[2]])
    #     return value

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

        """
        self.mod_health(value)

    def take_damage(self, value, type_):
        for feat in self.feats:
            if feat["category"] == "passive":
                if (feat["type"] == "vulnerability"
                        and feat["modifies"] == type_):
                    value *= 2
                if (feat["type"] == "resistance"
                        and feat["modifies"] == type_):
                    value /= 2

        self.mod_health(-value)

    # def ability_check(self, ability, roll, proficiency=False):
    #     roll += self.ability_mod(ability)
    #     if ability in self.proficiencies:
    #         roll += self.proficiency_bonus
    #     if ability not in self.proficiencies and proficiency is True:
    #         roll += self.proficiency_bonus

    def has_proficiency(self, proficiency):
        if proficiency in self.proficiencies:
            return True
        else:
            return False

    # def tool_check(self, ability, tool, roll, proficiency=False):
    #     roll += self.ability_mod(ability)
    #     if tool in self.inventory and self.have_tool_proficiency(tool):
    #         roll += self.proficiency_bonus
    #     if tool not in self.proficiencies and proficiency is True:
    #         roll += self.proficiency_bonus

    # def weapon_attack_roll(self, weapon, ability='str')

    # Ignore literally all of this for now. Only work on displaying info.

    # TODO inventory search, add, remove
    # TODO attacks using skill check (handle dex vs str attacks)
        # has to check all feats for modifying attack rolls
        # takes arguments for weapon (check if weapon modifies)
        # as well as skill, melee or ranged, etc etc
    # TODO add max spell slots property and spell slots variable

    """TODO spellcasting system

    depends on a lot of things, so, steps:
    - make structure for spell in spells json
    - make character known spells based on this
        - add tag that determines which class has that spell for calc
    - spellcasting method takes spell and level to cast at, option to roll dmg
        - auto update available spell slots, raise exception if can't cast
    """

    # TODO implement basically all number usage using xdice
