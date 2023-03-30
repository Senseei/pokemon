import requests

class Type:
    def __init__(self, typeinfo):
        self.properties = typeinfo
        self.name = self.properties["name"]

    def __eq__(self, other):
        return self.name == other.name

    @classmethod
    def setDamageRelations(cls, type_objects):
        dict = {}
        dict["double_damage_from"] = []
        dict["half_damage_from"] = []
        dict["no_damage_from"] = []

        for type_object in type_objects:
            for key in type_object.properties["damage_relations"]:
                if key in ["double_damage_from", "half_damage_from", "no_damage_from"]:
                    for type in type_object.properties["damage_relations"][key]:
                        dict[key].append(type["name"])
        return dict

    @classmethod
    def check_effectiveness(cls, move, other_pokemon):
        effectiveness = 1
        for key in other_pokemon.damage_relations:
            if move.type.name in other_pokemon.damage_relations[key]:
                if key == "double_damage_from":
                    effectiveness = 2
                elif key == "half_damage_from":
                    effectiveness = 0.5
                elif key == "no_damage_from":
                    effectiveness = 0
        return effectiveness

    @classmethod
    def create_type(cls, type):
        if response:= requests.get("https://pokeapi.co/api/v2/type/" + type):
            return cls(response.json())