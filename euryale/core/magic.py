class Magic():

    def __init__(self, registry, cdata):
        self.spells_known = cdata.get("spells known")
        self._spells_prepared = cdata.get("spells prepared")
        self._spell_slots = cdata.get("spell slots")

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
