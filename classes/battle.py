import time
import requests
import random
from classes.move import Move

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
            Battle.show_options(self.player1)
            self.player1.setAction()
            Battle.show_options(self.player2)
            self.player2.setAction()
            time.sleep(1)
            # check if some move has priority
            self.setActionPriority()

            # starts the queue
            for current_player in self.queue:
                print(f"It's {current_player.nickname}'s {current_player.getActivePokemon().getName()}'s turn!")
                self.turns += 1

                # defines the current_player and the other to execute their actions
                if current_player.getActivePokemon() == self.player1.getActivePokemon():
                    other_player = self.player2
                else:
                    other_player = self.player1

                # checks and actives the current status of the pokemon. Paralyze, for example, and if so, returns True or False if the player will play on this turn, or not
                if self.check_pokemon_status(current_player.getActivePokemon(), other_player.getActivePokemon()) or current_player.action in ["bag", "pokemons"]:
                    self.execute_action(current_player, other_player)
                self.show_pokemons()
                time.sleep(2)

                # checks if there are any fainted pokemons
                if fainted_pokemons:= self.check_lives():
                    for p in fainted_pokemons:
                        print(f"{p['pokemon'].getName()} has fainted!")
                        if not self.check_winner():
                            self.switch_pokemon(p["player"])

                    # checks the pokemon lives and if there is a winner
                    if self.check_winner():
                        self.in_progress = False
                        time.sleep(1)
                        if self.winner:
                            print(f"{self.loser.nickname} is out of pokemons..")
                            print(f"{self.winner.nickname} is the winner!")
                        else:
                            print(f"Both players are out of pokemons!")
                            print(f"It's a draw!")
                        break
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

    def check_pokemon_status(self, pokemon, other_pokemon):
        will_play = True
        for status in pokemon.status:
            success_chance = random.randint(1, 10000) / 10000
            if status.name == "badly poison":
                damage = status.damage * pokemon.getHealth() * status.damage_multiplier
                if damage > status.max_damage:
                    damage = status.max_damage
                pokemon.decreaseHealth(damage)
                print(f"{status.toString('during')}")
                status.damage_multiplier += 1
            elif status.name == "sleep":
                if success_chance > status.effect_chance():
                    pokemon.removeStatus("sleep")
                    print(f"{pokemon.owner}'s {pokemon.getName()} woke up!")
                else:
                    print(f"{status.toString('during')}")
                    will_play = False
            elif status.name == "freeze" or status.name == "paralyze":
                if success_chance <= status.effect_chance:
                    print(f"{status.toString('during')}")
                    will_play = False
            else:
                if success_chance <= status.effect_chance():
                    pokemon.decreaseHealth(status.damage * pokemon.getHealth() * status.damage_multiplier)
                    print(f"{status.toString('during')}")
        return will_play


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
                self.switch_pokemon(player, back=True)
            case "bag":
                player.list_bag()

    # checks if the pokemons are still alive
    def check_lives(self):
        fainted_pokemons = []
        if self.player1.getActivePokemon().getHealth(stat="current") <= 0:
            fainted_pokemons.append({"player": self.player1, "pokemon": self.player1.getActivePokemon()})
            self.player1.updateAlivePokemonsFromTeam(-1)
        if self.player2.getActivePokemon().getHealth(stat="current") <= 0:
            fainted_pokemons.append({"player": self.player2, "pokemon": self.player2.getActivePokemon()})
            self.player2.updateAlivePokemonsFromTeam(-1)
        return fainted_pokemons

    # checks if the pokemons are still alive and switches the player active pokemon, or returns a winner if there is no more alive pokemons in the team
    def check_winner(self):
        if self.player1.getAlivePokemonsFromTeam() == 0 and self.player2.getAlivePokemonsFromTeam() == 0:
            return True
        if self.player1.getAlivePokemonsFromTeam() == 0:
            self.winner = self.player2
            self.loser = self.player1
            return True
        if self.player2.getAlivePokemonsFromTeam() == 0:
            self.winner = self.player1
            self.loser = self.player2
            return True
        return False

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

    # switches the player's pokemon
    def switch_pokemon(self, player, back=False):
        time.sleep(1)
        print(f"{player.nickname}'s pokemons:")
        print(player.list_pokemons("battle"))
        while True:
            if back:
                action = input("Select the pokemon.. or type 'back' to go back.. ").lower()
                for pokemon in player.getPokemonsFromTeam():
                    if action == pokemon.name and pokemon.getHealth("current") > 0:
                        player.active_pokemon = pokemon
                        print(f"{player.nickname} chose {pokemon.getName()}!")
                        return
                    elif action == pokemon.name and pokemon.getHealth("current") == 0:
                        print(f"{pokemon.getName()} cannot fight..")
                if action == "back":
                    self.queue = sorted([self.player1, self.player2], reverse=True, key=lambda player: player.getActivePokemon().getSpeed("current"))
                    player.setAction()
                    self.setActionPriority()
                    if player == self.player1:
                        other_player = self.player2
                    else:
                        other_player = self.player1
                    self.execute_action(player, other_player)
                    return
            else:
                pokemon_name = input("Select the pokemon.. ").lower()
                for pokemon in player.getPokemonsFromTeam():
                    if pokemon_name == pokemon.name and pokemon.getHealth("current") > 0:
                        player.active_pokemon = pokemon
                        print(f"{player.nickname} chose {pokemon.getName()}!")

                        return
                    elif pokemon_name == pokemon.name and pokemon.getHealth("current") == 0:
                        print(f"{pokemon.getName()} cannot fight..")

    def show_players(self):
        print(f"{self.player1}")
        time.sleep(1)
        print("Versus\n")
        time.sleep(1)
        print(f"{self.player2}")

    @classmethod
    def show_options(cls, player):
        fstring = "| "
        for move in player.getActivePokemon().getMoves():
            fstring += f"[{move.name}] "
        for option in ["pokemons", "bag"]:
            fstring += f"[{option}] "
        fstring += "|\n"
        table_length = len(fstring) - 1
        print(f"{'-' * table_length}\n{fstring}{'-' * table_length}")

    @classmethod
    def setTargets(cls):
        targets = []
        for i in range(1, 17):
            targets.append(requests.get("https://pokeapi.co/api/v2/move-target/" + str(i)).json())
        return targets

    @classmethod
    def start_battle(cls, player1, player2):
        battle = cls(player1, player2)
        battle.show_players()
        battle.battle()
        return battle