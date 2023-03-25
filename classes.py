import requests
import random
import time

class Battle:
    def __init__(self, player1, player2):
        self.turns = 0
        self.player1 = player1
        self.player2 = player2
        self.winner = None
        self.loser = None
        self.targets = Battle.setTargets()
        self.in_progress = True

    # Simulates a 1x1 battle
    def battle(self):
        # a loop that will end only when a pokemon faint
        while self.in_progress:
            # defines a queue sorted by speed
            self.queue = sorted([self.player1, self.player2], reverse=True, key=lambda player: player.getActivePokemon().getSpeed("current"))

            # gets what the players want to do
            self.player1.setAction()
            self.player2.setAction()
            time.sleep(1)
            # check if some move has priority
            self.setActionPriority()

            # starts the queue
            for current_player in self.queue:
                print(f"It's {current_player.getActivePokemon().name.title()}'s turn!")
                self.turns += 1

                # defines the current_player and the other to execute their actions
                if current_player.getActivePokemon() == self.player1.getActivePokemon():
                    other_player = self.player2
                else:
                    other_player = self.player1

                self.execute_action(current_player, other_player)
                self.show_pokemons()
                time.sleep(2)

                # checks the pokemon lives and if there is a winner
                if self.check_winner():
                    self.in_progress = False
                    time.sleep(1)
                    print(f"{self.loser.nickname} is out of pokemons..")
                    print(f"{self.winner.nickname} is the winner!")
                    break

    # check if the player's action has priority
    def setActionPriority(self):
        if Move.isMove(self.player1.action) and Move.isMove(self.player2.action):
            move1p = self.player1.getActivePokemon().moves[self.player1.action].getPriority()
            move2p = self.player2.getActivePokemon().moves[self.player2.action].getPriority()
            # if both have priority, the queue does not change
            if move1p == 1 and move2p == 1:
                return
        if Move.isMove(self.player1.action):
            if self.player1.getActivePokemon().moves[self.player1.action].getPriority() == 1:
                self.queue = [self.player1, self.player2]
                return
        if Move.isMove(self.player2.action):
            if self.player2.getActivePokemon().moves[self.player2.action].getPriority() == 1:
                self.queue = [self.player2, self.player1]

        # checks if the player wants to change their pokemon
        if self.player1.action == "pokemons" and self.player2.action == "pokemons":
            return
        elif self.player1.action == "pokemons":
            self.queue = [self.player1, self.player2]
        elif self.player2.action == "pokemons":
            self.queue = [self.player2, self.player1]
        return

    # executes the player's action, and calls its respective method
    def execute_action(self, player, other_player):
        action = player.action
        moves = player.getActivePokemon().getMoves()
        for move in moves:
            if move.name == action:
                player.action = move
                time.sleep(1)
                print(f"{player.getActivePokemon().getName()} used {player.action.name}..")
                Move.execute_move(player.action, player.getActivePokemon(), other_player.getActivePokemon())
                return
        match action:
            case "pokemons":
                print(player.list_pokemons("battle"))
            case "bag":
                player.list_bag()

    # checks if the pokemons are still alive and switches the player active pokemon, or returns a winner if there is no more alive pokemons in the team
    def check_winner(self):
        current_player = self.queue[0]
        other_player = self.queue[1]

        if current_player.getActivePokemon().getHealth("current") <= 0:
            time.sleep(1)
            print(f"{current_player.getActivePokemon().getName()} has fainted!")
            current_player.alive_pokemons -= 1
            if current_player.alive_pokemons > 0:
                Battle.switch_pokemon(current_player)
            else:
                self.winner = other_player
                self.loser = current_player
                return True
        if other_player.getActivePokemon().getHealth("current") <= 0:
            time.sleep(1)
            print(f"{other_player.getActivePokemon().getName()} has fainted!")
            other_player.alive_pokemons -= 1
            if other_player.alive_pokemons > 0:
                Battle.switch_pokemon(other_player)
            else:
                self.winner = current_player
                self.loser = other_player
                return True

    def show_pokemons(self):
        fstring = ""
        pokemon1 = self.player1.getActivePokemon()
        pokemon2 = self.player2.getActivePokemon()

        table_length = 26
        space_between = " " * 5
        div = ("-" * table_length) + space_between + ("-" * table_length) + "\n"
        fstring = ""

        fstring += div
        fstring += f"| {pokemon1}{' ' * (table_length - len(str(pokemon1)) - 3)}|" + space_between + f"| {pokemon2}{' ' * (table_length - len(str(pokemon2)) - 3)}|\n"
        lifebar1 = round(20 * pokemon1.getHealth(stat="current") / pokemon1.getHealth())
        lifebar2 = round(20 * pokemon2.getHealth(stat="current") / pokemon2.getHealth())
        fstring += f"| [{'=' * lifebar1}{' ' * (20 - lifebar1)}] |" + space_between + f"| [{'=' * lifebar2}{' ' * (20 - lifebar2)}] |\n"
        hp1 = f"HP: {pokemon1.getHealth(stat='current')}/{pokemon1.getHealth()}"
        hp2 = f"HP: {pokemon2.getHealth(stat='current')}/{pokemon2.getHealth()}"
        fstring += f"| {hp1}{' ' * (table_length - len(hp1) - 3)}|" + space_between + f"| {hp2}{' ' * (table_length - len(hp2) - 3)}|\n"

        fstring += div
        print(fstring)

    @classmethod
    def setTargets(cls):
        targets = []
        for i in range(1, 17):
            targets.append(requests.get("https://pokeapi.co/api/v2/move-target/" + str(i)).json())
        return targets

    # switches the player's pokemon
    @classmethod
    def switch_pokemon(cls, player):
        time.sleep(1)
        print(f"{player.nickname}'s pokemons:")
        print(player.list_pokemons("battle"))
        while True:
            pokemon_name = input("Select the pokemon.. ")
            for pokemon in player.pokemons:
                if pokemon_name == pokemon.name:
                    player.active_pokemon = pokemon
                    break
            print("Invalid pokemon")

    @classmethod
    def start_battle(cls, player1, player2):
        battle = cls(player1, player2)
        battle.battle()
        return battle


class Player:
    def __init__(self, nickname, pokemons=[], bag=[]):
        if not nickname:
            print("Insert a nickname")
            raise ValueError

        self.pokemons = pokemons
        self.active_pokemon = self.pokemons[0]
        self.alive_pokemons = len(self.pokemons)
        self.nickname = nickname
        self.bag = bag

    def __str__(self):
        return f"{self.nickname}'s pokemons:\n" + self.list_pokemons()

    # lists all the pokemons the player has
    def list_pokemons(self, details=""):
        # checks what kind of information the user may see
        if details == "stats":
            # prints a table with the pokemon's name followed by its stats
            table_length = 30
            div = "-" * table_length + "\n"
            fstring = ""

            for pokemon in self.pokemons:
                hp, atq, df = str(pokemon.getHealth()), str(pokemon.getAttack()), str(pokemon.getDefense())
                spatq, spdef, spd = str(pokemon.getSpecial_attack()), str(pokemon.getSpecial_defense()), str(pokemon.getSpeed())
                margin = (table_length - len(str(pokemon)) - 2) // 2
                fstring += div
                if len(str(pokemon)) % 2 == 0:
                    fstring += f"|{' ' * margin}{pokemon}{' ' * margin}|\n"
                else:
                    fstring += f"|{' ' * margin}{pokemon}{' ' * (margin + 1)}|\n"
                fstring += div
                fstring += f"| HP: {hp}{' ' * (table_length - len(f'HP: ATQ: {hp + atq}') - 4)}ATQ: {atq} |\n"
                fstring += f"| DEF: {df}{' ' * (table_length - len(f'DEF: SPATQ: {df + spatq}') - 4)}SPATQ: {spatq} |\n"
                fstring += f"| SPDEF: {spdef}{' ' * (table_length - len(f'SPDEF: SPD: {spdef + spd}') - 4)}SPD: {spd} |\n"

            fstring += div
            return fstring
        elif details == "battle":
            # prints a table with the pokemon's name followed by its hp with a fancy hp bar
            table_length = 26
            div = "-" * table_length + "\n"
            fstring = ""

            for pokemon in self.pokemons:
                fstring += div
                fstring += f"| {pokemon}{' ' * (table_length - len(str(pokemon)) - 3)}|\n"
                life = round(20 * pokemon.getHealth(stat="current") / pokemon.getHealth())
                fstring += f"| [{'=' * life}{' ' * (20 - life)}] |\n"
                hp = f"HP: {pokemon.getHealth(stat='current')}/{pokemon.getHealth()}"
                fstring += f"| {hp}{' ' * (table_length - len(hp) - 3)}|\n"

            fstring += div
            return fstring
        else:
            # prints a table with just the pokemon's names
            larger_name = 0
            higher_level = 0
            for pokemon in self.pokemons:
                if len(pokemon.name) > larger_name:
                    larger_name = len(pokemon.name)
                if pokemon.level > higher_level:
                    higher_level = pokemon.level

            table_length = larger_name + len(f"Lvl {higher_level}") + 7
            div = "-" * table_length + "\n"
            fstring = div
            for pokemon in self.pokemons:
                margin_right = larger_name + 1 - len(pokemon.name)
                fstring += f"| {pokemon}{' ' * margin_right }|\n"

        fstring += div
        return fstring

    def list_bag(self):
        ...

    # gets the player's active pokemon
    def getActivePokemon(self):
        return self.active_pokemon

    # method responsible for checking the users input and set the player's action, if it's valid
    def setAction(self):
        while True:
            actions = ["bag", "pokemons"] + self.getActivePokemon().getMoves(str=True)
            action = input(f"What to do now, {self.nickname}?.. ").lower()
            if action not in actions:
                print("Invalid action")
                continue
            self.action = action
            break

    # Creates a new player
    @classmethod
    def create_player(cls):
        # asks for a valid nickname
        while True:
            if nickname:= input("Insert your nickname: "):
                break

        # creates an empty list of pokemons with max length 6
        pokemons = []
        while len(pokemons) < 6:
            try:
                pokemons.append(Pokemon.create_pokemon())
            except EOFError:
                print("\n")
                break
            except:
               continue
        return cls(nickname, pokemons)

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
        self.evasiveness = 1
        self.accuracy = 1

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
        return self.accuracy

    def getEvasiveness(self):
        return self.evasiveness

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


class Stat:
    def __init__(self, stat_info, stat):
        self.name = stat_info["stat"]["name"]
        self.base_stat = stat_info["base_stat"]
        self.iv = random.randint(0,31)
        self.ev = stat_info["effort"]
        self.stat = stat
        self.stat_level = 0
        self.current_stat = stat

    def __lt__(self, other):
        return self.stat > other.stat

    def __eq__(self, other):
        return self.stat == other.stat

    def getName(self):
        return self.name

    def getBaseStat(self):
        return self.base_stat

    def getIV(self):
        return self.iv

    def getEV(self):
        return self.ev

    def getStat(self):
        return self.stat

    def getCurrentStat(self):
        return self.current_stat

    def change_stat(self, level):
        negative_stat_level_table = {
            -6: 0.25,
            -5: 0.29,
            -4: 0.33,
            -3: 0.40,
            -2: 0.50,
            -1: 0.66
        }
        self.stat_level += level
        if self.stat_level >= 0:
            self.current_stat *= (1 + self.stat_level / 2)
        else:
            self.current_stat *= negative_stat_level_table[self.stat_level]

    # sets the EV points of the current stat, and check if it's valid
    @classmethod
    def setEV(cls, stat):
        while True:
            try:
                value = int(input(f"Set {stat} Effort Value: "))
                if not 0 <= value <= 252:
                    raise ValueError
                return value
            except ValueError:
                print("Invalid value, insert a number between 1 and 252")

    # calculates the stat based on the pokemon's level
    @classmethod
    def setStat(cls, stat_info, level):
        base_stat = stat_info["base_stat"]
        iv = random.randint(0,31)
        ev = stat_info["effort"]
        if stat_info["stat"]["name"] == "hp":
            stat = round(((((2 * base_stat) + iv + (ev/4)) * level) / 100) + level + 10)
        elif stat_info["stat"]["name"] in ["accuracy", "evasion"]:
            stat = base_stat
        else:
            stat = round((((((2 * base_stat) + iv + (ev/4)) * level) / 100) + 5))
        # returns the stat object
        return cls(stat_info, stat)


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
        for key in other_pokemon.damage_relations:
            if move.type.name in other_pokemon.damage_relations[key]:
                if key == "double_damage_from":
                    return 2
                elif key == "half_damage_from":
                    return 0.5
                elif key == "no_damage_from":
                    return 0
        return 1

    @classmethod
    def create_type(cls, type):
        if response:= requests.get("https://pokeapi.co/api/v2/type/" + type):
            return cls(response.json())


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
        if random.randint(1, 10000) / 10000 <= pokemon.getCritChance():
            critical = 1.5
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