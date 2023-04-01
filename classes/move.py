from classes.type import Type
from classes.status import Status
import time
import random
import requests

class Move:
    def __init__(self, moveinfo):
        self.properties = moveinfo
        self.name = self.properties["name"]
        self.type = Type.create_type(self.properties["type"]["name"])
        self.damage_class = self.properties["damage_class"]["name"]
        self.effects = Move.setEffectInfo(self.properties)
        self.stat_changes = Move.setStatChanges(self.properties)
        self.power = self.properties["power"]
        self.pp = self.properties["pp"]
        self.accuracy = self.properties["accuracy"]
        self.target = self.properties["target"]["name"]

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def apply_effects(self, pokemon):
        time.sleep(1)
        status = ["paralyze", "freeze", "burn", "poison", "badly poison", "sleep"]
        for status_effect in status:
            for effect in self.effects:
                if status_effect in effect.lower():
                    if (not self.getEffectChance() or random.randint(1, 100) <= self.getEffectChance()):
                        status = Status.setStatus(status_effect, pokemon)
                        if status not in pokemon.status:
                            pokemon.status.append(status)
                            print(f"{status.toString()}")
        if not self.getEffectChance() or random.randint(1, 100) <= self.getEffectChance():
            for stat in self.stat_changes:
                pokemon.updateStatLevel(stat, self.stat_changes[stat]["change"])
                print(f"{pokemon.owner}'s {pokemon.getName()}'s {self.stat_changes[stat]['effect_entry']}")


    def getPriority(self):
        return self.properties["priority"]

    def getName(self):
        return self.name

    def getType(self):
        return self.type

    def getDamageClass(self):
        return self.damage_class

    def getPower(self):
        if self.power:
            return self.power
        else:
            return 0

    def getPP(self):
        return self.pp

    def getAccuracy(self):
        return self.accuracy

    def getEffectChance(self):
        if ec:= self.properties["effect_chance"]:
            return ec

    def decreasePP(self, pp):
        self.pp -= pp

    @classmethod
    def getHitChance(cls, move, pokemon, other_pokemon):
        if not move.getAccuracy():
            return 100
        else:
            return move.getAccuracy() * (pokemon.getAccuracy() / other_pokemon.getEvasiveness())

    @classmethod
    def setEffectInfo(cls, moveinfo):
        effects = []
        for effect in moveinfo["effect_entries"]:
            effects.append(effect["effect"])
        return effects

    @classmethod
    def setStatChanges(cls, moveinfo):
        stats = {}
        for stat in moveinfo["stat_changes"]:
            stat_name = stat["stat"]["name"]
            tmpdict = {}
            tmpdict["change"] = stat["change"]
            if stat["change"] > 0:
                tmpdict["effect_entry"] = f"{stat_name} has been raised!"
            elif stat["change"] < 0:
                tmpdict["effect_entry"] = f"{stat_name} has been decreased!"

            stats[stat_name] = tmpdict
        return stats

    @classmethod
    def execute_move(cls, move, pokemon, other_pokemon):
        if random.randint(1, 100) > Move.getHitChance(move, pokemon, other_pokemon):
            move.decreasePP(1)
            print(f"{other_pokemon.getName()} avoided the attack!")
            return False
        else:
            move.decreasePP(1)
            if move.getDamageClass() != "status":
                damage_summary = Move.calculate_damage(move, pokemon, other_pokemon)
                if effectiveness:= damage_summary["effectiveness"]:
                    time.sleep(0.5)
                    match effectiveness:
                        case "super-effective":
                            print("It was super effective!")
                        case "not-effective":
                            print("It was not very effective...")
                        case "does not affect":
                            print(f"It does not affect {other_pokemon.getName()}...")
                if damage_summary["critical"]:
                    time.sleep(1)
                    print("A critical hit!")
                other_pokemon.decreaseHealth(damage_summary["damage"])

            if move.target == "user":
                move.apply_effects(pokemon)
            else:
                move.apply_effects(other_pokemon)
            time.sleep(1)
            return True

    @classmethod
    def calculate_damage(cls, move, pokemon, other_pokemon):
        summary = {}
        effectiveness = Type.check_effectiveness(move, other_pokemon)
        if effectiveness == 2:
            summary["effectiveness"] = "super-effective"
        elif effectiveness == 0.5:
            summary["effectiveness"] = "not-effective"
        elif effectiveness == 0:
            summary["effectiveness"] = "does not affect"
        else:
            summary["effectiveness"] = "normal"

        match move.damage_class:
            case "physical":
                atkstat = pokemon.getAttack("current_stat")
                defstat = pokemon.getDefense("current_stat")
            case "special":
                atkstat = pokemon.getSpecialAttack("current_stat")
                defstat = pokemon.getSpecialDefense("current_stat")
        stab = 1
        if move.getType() in pokemon.getTypes():
            stab = 1.5
        critical = 1
        summary["critical"] = False
        if random.randint(1, 10000) / 10000 <= pokemon.getCritChance() and effectiveness != 0:
            critical = 2
            summary["critical"] = True
        other = 1
        summary["damage"] = round(((((2*pokemon.level/5+2)*atkstat*move.power/defstat)/50)+2)*stab*effectiveness*critical*other*(80/100))
        return summary

    # checks if the move exist
    @classmethod
    def isMove(cls, move):
        if requests.get("https://pokeapi.co/api/v2/move/" + str(move)):
            return True
        return False

    # creates a movement
    @classmethod
    def create_move(cls):
        if move_id:= input("Move ID: "):
            # check if the move exist and get all its information
            if response:= requests.get("https://pokeapi.co/api/v2/move/" + move_id):
                # returns the move object
                return cls(response.json())