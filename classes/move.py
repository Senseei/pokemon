from classes.type import Type
import time
import random
import requests

class Move:
    def __init__(self, moveinfo):
        self.properties = moveinfo
        self.name = self.properties["name"]
        self.type = Type.create_type(self.properties["type"]["name"])
        self.damage_class = self.properties["damage_class"]["name"]
        self.effect = Move.setEffectInfo(self.properties)
        self.power = self.properties["power"]
        self.pp = self.properties["pp"]
        self.accuracy = self.properties["accuracy"]

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def apply_effects(self, pokemon):
        ...

    def getPriority(self):
        return self.properties["priority"]

    def getName(self):
        return self.name

    def getType(self):
        return self.type

    def getDamageClass(self):
        return self.damage_class

    def getPower(self):
        return self.power

    def getPP(self):
        return self.pp

    def getAccuracy(self):
        return self.accuracy

    def decreasePP(self, pp):
        self.pp -= pp

    @classmethod
    def setEffectInfo(cls, moveinfo):
        dict = {"effect_chance": moveinfo["meta"]["ailment_chance"], "effect": moveinfo["meta"]["ailment"]["name"], "stat_change_chance": moveinfo["meta"]["stat_chance"], "stat_changes": moveinfo["stat_changes"]}
        list = []
        for change in moveinfo["stat_changes"]:
            change["stat"] = change["stat"]["name"]
            list.append(change)
        dict["stat_changes"] = list
        if dict["effect_chance"] == 0:
            dict["effect_chance"] = 100
        return dict

    @classmethod
    def execute_move(cls, move, pokemon, other_pokemon):
        if not move.getAccuracy():
            hit_chance = 100
        else:
            hit_chance = move.getAccuracy() * (pokemon.getAccuracy() / other_pokemon.getEvasiveness())
        if random.randint(1, 100) > hit_chance:
            move.decreasePP(1)
            print(f"{other_pokemon.getName()} avoided the attack!")
            return False
        else:
            move.decreasePP(1)
            move.apply_effects(other_pokemon)
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