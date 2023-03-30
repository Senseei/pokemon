import requests
from classes.type import Type
from classes.stat import Stat
from classes.move import Move

class Pokemon:
    def __init__(self, pokemoninfo):
        self.properties = pokemoninfo
        self.name = self.properties["name"]
        self.types = self.setTypes(self.properties["types"])
        self.level = int(self.properties["level"])
        self.moves = self.properties["current_moves"]
        # Pokemon's stats
        self.stats = Pokemon.defineStats(pokemoninfo, self.level)
        # Pokemon's type relations
        self.damage_relations = Type.setDamageRelations(self.types)
        self.crit_chance = 0.0625

    def __str__(self):
        return f"Lvl {self.level} - {self.getName()}"

    def __eq__(self, other):
        return self.name == other.name

    # gets the current, or full stats of the pokemon
    def getHealth(self, stat=""):
        if stat == "current":
            return self.stats["hp"].current_stat
        else:
            return self.stats["hp"].stat

    def getAttack(self, stat=""):
        if stat == "current":
            return self.stats["attack"].current_stat
        else:
            return self.stats["attack"].stat

    def getDefense(self, stat=""):
        if stat == "current":
            return self.stats["defense"].current_stat
        else:
            return self.stats["defense"].stat

    def getSpecialAttack(self, stat=""):
        if stat == "current":
            return self.stats["special-attack"].current_stat
        else:
            return self.stats["special-attack"].stat

    def getSpecialDefense(self, stat=""):
        if stat == "current":
            return self.stats["special-defense"].current_stat
        else:
            return self.stats["special-defense"].stat

    def getSpeed(self, stat=""):
        if stat == "current":
            return self.stats["speed"].current_stat
        else:
            return self.stats["speed"].stat

    def getCritChance(self):
        return self.crit_chance

    def getAccuracy(self):
        return self.stats["accuracy"].current_stat

    def getEvasiveness(self):
        return self.stats["evasion"].current_stat

    def getName(self):
        return f"{self.name.title()}"

    def getTypes(self):
        return self.types

    # gets the current moves of the pokemon
    def getMoves(self, str=False):
        moves = []
        # if str, it will return a list with the names of the moves
        if str:
            for move in self.moves:
                moves.append(move)
        # else, it will return a list with the objects
        else:
            for move in self.moves:
                moves.append(self.moves[move])
        return moves

    def getMoveByName(self, name):
        for move in self.moves:
            if move.name == name:
                return move

    def setTypes(self, types):
        object_types = []
        for type in types:
            object_types.append(Type.create_type(type["type"]["name"]))
        return object_types

    def decreaseHealth(self, damage_given):
        self.stats["hp"].current_stat -= damage_given
        if self.getHealth("current") < 0:
            self.stats["hp"].current_stat = 0

    @classmethod
    def defineStats(cls, pokemoninfo, pokemonlevel):
        stats = {}
        for stat in pokemoninfo["stats"]:
            stats[stat["stat"]["name"]] = Stat.setStat(stat, pokemonlevel)
        for stat in ["accuracy", "evasion"]:
            statinfo = {"base_stat": 1, "effort": 0, "stat": {"name": stat, "url": f"https://pokeapi.co/api/v2/stat/{stat}"}}
            stats[stat] = Stat.setStat(statinfo, pokemonlevel)
        return stats

    # Creates a pokemon
    @classmethod
    def create_pokemon(cls):
        pokemon = input("Pokemon's name: ").lower()
        # checks if the pokemon exists. If it exists, get all the information of the pokemon
        if response:= requests.get("https://pokeapi.co/api/v2/pokemon/" + pokemon):
            try:
                level = int(input("Level: "))
            except:
                print("Invalid level")
                raise TypeError
            else:
                if not (0 < level <= 100):
                    print("Level must be a number between 1 and 100")
                    raise ValueError

            pokemoninfo = response.json()

            # sets the moves of the pokemons
            moves = {}
            while len(moves) < 4:
                if move:= Move.create_move():
                    # if the move is valid, it will check if the pokemon in fact can learn the move
                    if cls.is_learnable(move, pokemon) and move.name not in moves:
                        moves[move.name] = move
                    # checks if the pokemon has already learned the move
                    elif move.name in moves:
                        print(f"{pokemon.title()} has already learned this movement")
                    else:
                        print(f"{pokemon.title()} cannot learn this movement")
                else:
                    print("Please, insert a valid movement ID")

            # gives the option to set other properties of the pokemon
            remaining_evs = 504
            for i in range(6):
                remaining_evs -= pokemoninfo["stats"][i]["effort"]

            if answer:= input("Would like to change the EV of the stats? (optional): ") and answer.upper() == "YES":
                for i in range(6):
                    evs_used = Stat.setEV(pokemoninfo["stats"][i]["stat"]["name"])
                    if remaining_evs > 0 and evs_used <= remaining_evs:
                        pokemoninfo["stats"][i]["effort"] = evs_used
                        remaining_evs -= evs_used
                    else:
                        print("Not enough EVs..")

            # updates the pokemon info
            pokemoninfo.update({"level": level, "current_moves": moves})
            # returns the pokemon object
            return cls(pokemoninfo)
        else:
            print(f"{pokemon} does not exist")
            raise ValueError

    # method to check if the move is learnable by the pokemon
    @classmethod
    def is_learnable(cls, move, pokemon):
        for p in move.properties["learned_by_pokemon"]:
            if p["name"] == pokemon:
                return True
        return False