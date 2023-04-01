STATUS = {
    "paralyze": {
        "name": "paralyze",
        "damage": 0,
        "effect-chance": 0.25,
        "when_applied": "has been paralyzed..",
        "during": "is paralyzed.\nIt can't move!"
    },
    "freeze": {
        "name": "freeze",
        "damage": 0,
        "effect-chance": 0.25,
        "when_applied": "has been frozen..",
        "during": "is frozen.\nIt can't move!"
    },
    "burn": {
        "name": "burn",
        "damage": 0.0625,
        "effect-chance": 1,
        "when_applied": "is burning..",
        "during": "is hurt by its burn!"
    },
    "poison": {
        "name": "poison",
        "damage": 0.0625,
        "effect-chance": 1,
        "when_applied": "has been poisoned..",
        "during": "is hurt by poison!"
    },
    "badly poison": {
        "name": "bad-poison",
        "damage": 0.0625,
        "effect-chance": 1,
        "multiplier": 1,
        "when_applied": "has been badly poisoned!",
        "during": "is hurt by poison!"
    },
    "sleep": {
        "name": "sleep",
        "damage": 0,
        "effect-chance": 0.7,
        "when_applied": "fell asleep..",
        "during": "is still sleeping.."
    }
}

class Status:
    def __init__(self, statusinfo, pokemon):
        self.name = statusinfo["name"]
        self.pokemon = pokemon
        self.damage = statusinfo["damage"]
        self.damage_multiplier = statusinfo["multiplier"]
        self.effect_chance = statusinfo["effect-chance"]
        self.max_damage = statusinfo["max-damage"]
        self.strings = {"when_applied": statusinfo["when_applied"], "during": statusinfo["during"]}

    def __eq__(self, other):
        return self.name == other.name

    def toString(self, key="when_applied"):
        return f"{self.pokemon.owner}'s {self.pokemon.getName()} {self.strings[key]}"

    @classmethod
    def setStatus(cls, status, pokemon):
        statusinfo = STATUS[status]
        if status == "badly poison":
            statusinfo.update({"max-damage": 15 * (pokemon.getHealth()/16)})
            statusinfo
        else:
            statusinfo.update({"multiplier": 1, "max-damage": None})
        return cls(statusinfo, pokemon)