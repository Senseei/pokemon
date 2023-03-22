import requests
import random

class Battle:
    def __init__(self, player1, player2):
        self.turns = 0
        self.player1 = player1
        self.player2 = player2

    # Simulates a 1x1 battle
    def battle(self):
        # a loop that will end only when a pokemon faint
        while True:
            # defines a queue sorted by speed
            self.queue = sorted([self.player1, self.player2], reverse=True, key=lambda player: player.getActivePokemon().speed)

            # gets what the players want to do
            self.player1.setAction()
            self.player2.setAction()
            # check if some move has priority
            self.setMovePriority()

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

                # checks if there are any fainted pokemons
                if fainted_pokemons:= self.check_lives():
                    for p in fainted_pokemons:
                        print(f"{p['pokemon'].getName()} has fainted!")
                        self.switch_pokemon(p["player"])

    # check if the player's action has priority
    def setMovePriority(self):
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
        return

    # executes the player's action, and calls its respective method
    def execute_action(self, player, other_player):
        action = player.action
        moves = player.getActivePokemon().getMoves()
        for move in moves:
            if move.name == action:
                return self.execute_move(move)
        match action:
            case "leave":
                self.leave()
            case "pokemon":
                player.list_pokemons()
            case "bag":
                player.list_bag()


    def execute_move(self, move):
        ...

    def leave(self):
        ...

    # checks if the pokemons are still alive
    def check_lives(self):
        fainted_pokemons = []
        if self.player1.getActivePokemon().getHealth(stat="current") <= 0:
            fainted_pokemons.append({"player": self.player1, "pokemon": self.player1.getActivePokemon()})
            self.player1.alive_pokemons -= 1
        if self.player2.getActivePokemon().getHealth(stat="current") <= 0:
            fainted_pokemons.append({"player": self.player2, "pokemon": self.player2.getActivePokemon()})
            self.player2.alive_pokemons -= 1
        return fainted_pokemons

    # switches the player's pokemon
    def switch_pokemon(self, player):
        ...


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
        self.active_pokemon = 0
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

    # gets the player's active pokemon
    def getActivePokemon(self):
        return self.pokemons[self.active_pokemon]

    # method responsible for checking the users input and set the player's action, if it's valid
    def setAction(self):
        while True:
            actions = ["leave", "bag", "pokemons"] + self.getActivePokemon().getMoves(str=True)
            action = input(f"What to do now, {self.nickname}?.. ")
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
        self.level = int(self.properties["level"])
        self.moves = self.properties["current_moves"]
        self.health = Stat.setStat(self.properties["stats"][0], self.level)
        self.attack = Stat.setStat(self.properties["stats"][1], self.level)
        self.defense = Stat.setStat(self.properties["stats"][2], self.level)
        self.special_attack = Stat.setStat(self.properties["stats"][3], self.level)
        self.special_defense = Stat.setStat(self.properties["stats"][4], self.level)
        self.speed = Stat.setStat(self.properties["stats"][5], self.level)

    def __str__(self):
        return f"Lvl {self.level} - {self.getName()}"

    def __eq__(self, other):
        return self.name == other.name

    # gets the current, or full stats of the pokemon
    def getHealth(self, stat=""):
        if stat == "current":
            return self.health.current_stat
        else:
            return self.health.stat

    def getAttack(self, stat=""):
        if stat == "current":
            return self.attack.current_stat
        else:
            return self.attack.stat

    def getDefense(self, stat=""):
        if stat == "current":
            return self.defense.current_stat
        else:
            return self.defense.stat

    def getSpecial_attack(self, stat=""):
        if stat == "current":
            return self.special_attack.current_stat
        else:
            return self.special_attack.stat

    def getSpecial_defense(self, stat=""):
        if stat == "current":
            return self.special_defense.current_stat
        else:
            return self.special_defense.stat

    def getSpeed(self, stat=""):
        if stat == "current":
            return self.speed.current_stat
        else:
            return self.speed.stat

    def getName(self):
        return f"{self.name.title()}"

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
        self.current_stat = stat

    def __lt__(self, other):
        return self.stat > other.stat

    def __eq__(self, other):
        return self.stat == other.stat

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
        else:
            stat = round((((((2 * base_stat) + iv + (ev/4)) * level) / 100) + 5))
        # returns the stat object
        return cls(stat_info, stat)


class Move:
    def __init__(self, moveinfo):
        self.properties = moveinfo
        self.name = self.properties["name"]

    def __str__(self):
        return self.name

    def getPriority(self):
        return self.properties["priority"]

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
