import requests
import queue

class Battle:
    def __init__(self, player1, player2):
        self.turns = 0
        self.player1 = player1
        self.player2 = player2

    def battle(self):
        while True:
            self.queue = sorted([self.player1, self.player2], reverse=True, key=lambda player: player.pokemons[player.active_pokemon].properties["stats"][5]["base_stat"])

            self.player1.setAction()
            self.player2.setAction()
            self.setMovePriority()

            for current_player in self.queue:
                print(f"It's {current_player.pokemons[current_player.active_pokemon].properties['name'].title()}'s turn!")
                self.turns += 1
                #TODO
                if current_player.pokemons[current_player.active_pokemon] == self.player1.pokemons[self.player1.active_pokemon]:
                    other_player = self.player2
                else:
                    other_player = self.player1
                self.execute_action(current_player, current_player.action)


                if fainted_pokemons:= self.check_lives():
                    for p in fainted_pokemons:
                        print(f"{p['pokemon'].properties['name'].title()} has fainted!")
                        self.switch_pokemon(p["player"])

    def setMovePriority(self):
        if Move.isMove(self.player1.action) and Move.isMove(self.player2.action):
            move1p = self.player1.pokemons[self.player1.active_pokemon].properties["current_moves"][self.player1.action].getPriority()
            move2p = self.player2.pokemons[self.player2.active_pokemon].properties["current_moves"][self.player2.action].getPriority()
            if move1p == 1 and move2p == 1:
                return
        if Move.isMove(self.player1.action):
            if self.player1.pokemons[self.player1.active_pokemon].properties["current_moves"][self.player1.action].getPriority() == 1:
                self.queue = [self.player1, self.player2]
                return
        if Move.isMove(self.player2.action):
            if self.player2.pokemons[self.player2.active_pokemon].properties["current_moves"][self.player2.action].getPriority() == 1:
                self.queue = [self.player2, self.player1]
        return


    def execute_action(self, team, action):
        moves = team.pokemons[self.player1.active_pokemon].getMoves()
        for move in moves:
            if move.properties["name"] == action:
                return self.execute_move(move)
        match action:
            case "leave":
                self.leave()
            case "pokemon":
                self.list_pokemons()
            case "bag":
                self.list_bag()


    def execute_move(self, move):
        ...

    def leave(self):
        ...

    def list_pokemons(self):
        ...

    def list_bag(self):
        ...


    def check_lives(self):
        fainted_pokemons = []
        if self.player1.pokemons[self.player1.active_pokemon].properties["stats"][0]["base_stat"] <= 0:
            fainted_pokemons.append({"player": self.player1, "pokemon": self.player1.pokemons[self.player1.active_pokemon]})
            self.player1.alive_pokemons -= 1
        if self.player2.pokemons[self.player2.active_pokemon].properties["stats"][0]["base_stat"] <= 0:
            fainted_pokemons.append({"player": self.player2, "pokemon": self.player2.pokemons[self.player2.active_pokemon]})
            self.player2.alive_pokemons -= 1
        return fainted_pokemons

    def switch_pokemon(self, team):
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
        fstring = f"{self.nickname}'s pokemons:\n"
        for pokemon in self.pokemons:
             fstring += f"{pokemon}\n"
        return fstring

    def setAction(self):
        while True:
            actions = ["leave", "bag", "pokemons"] + self.pokemons[self.active_pokemon].getMoves(str=True)
            action = input("What to do now?.. ")
            if action not in actions:
                print("Invalid action")
                continue
            self.action = action
            break


    @classmethod
    def create_player(cls):
        while True:
            if nickname:= input("Insert your nickname: "):
                break

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

    def __str__(self):
        return f"Lvl {self.properties['level']} - {self.properties['name'].title()}"

    def __eq__(self, other):
        return self.properties["name"] == other.properties["name"]

    def getMoves(self, str=False):
        moves = []
        if str:
            for move in self.properties["current_moves"]:
                moves.append(move)
        else:
            for move in self.properties["current_moves"]:
                moves.append(self.properties["current_moves"][move])
        return moves

    @classmethod
    def create_pokemon(cls):
        pokemon = input("Pokemon's name: ").lower()
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

            moves = {}
            while len(moves) < 4:
                if move:= Move.create_move():
                    if cls.is_learnable(move, pokemon) and move.properties["name"] not in moves:
                        moves[move.properties["name"]] = move
                    elif move.properties["name"] in moves:
                        print(f"{pokemon.title()} has already learned this movement")
                    else:
                        print(f"{pokemon.title()} cannot learn this movement")
                else:
                    print("Please, insert a valid movement ID")

            pokemoninfo = response.json()
            pokemoninfo.update({"level": level, "current_moves": moves})
            return cls(pokemoninfo)
        else:
            print(f"{pokemon} does not exist")
            raise ValueError

    @classmethod
    def is_learnable(cls, move, pokemon):
        for p in move.properties["learned_by_pokemon"]:
            if p["name"] == pokemon:
                return True
        return False


class Move:
    def __init__(self, moveinfo):
        self.properties = moveinfo

    def __str__(self):
        return self.properties["name"]

    def getPriority(self):
        return self.properties["priority"]

    @classmethod
    def isMove(cls, move):
        if requests.get("https://pokeapi.co/api/v2/move/" + str(move)):
            return True
        return False

    @classmethod
    def create_move(cls):
        if move_id:= input("Move ID: "):
            if response:= requests.get("https://pokeapi.co/api/v2/move/" + move_id):
                return cls(response.json())
