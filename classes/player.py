import pickle
from classes.team import Team
from classes.globals import PROFILES_PATH

class Player:
    def __init__(self, nickname, teams=[], bag=[]):
        if not nickname:
            print("Insert a nickname")
            raise ValueError

        self.teams = teams
        self.active_team = self.teams[0]
        self.active_pokemon = self.getPokemonsFromTeam()[0]
        self.nickname = nickname
        self.bag = bag

    def __eq__(self, other):
        return self.nickname == other.nickname

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

            for pokemon in self.getPokemonsFromTeam():
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

            for pokemon in self.getPokemonsFromTeam():
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
            for pokemon in self.getPokemonsFromTeam():
                if len(pokemon.name) > larger_name:
                    larger_name = len(pokemon.name)
                if pokemon.level > higher_level:
                    higher_level = pokemon.level

            table_length = larger_name + len(f"Lvl {higher_level}") + 7
            div = "-" * table_length + "\n"
            fstring = div
            for pokemon in self.getPokemonsFromTeam():
                margin_right = larger_name + 1 - len(pokemon.name)
                fstring += f"| {pokemon}{' ' * margin_right }|\n"

        fstring += div
        return fstring

    def list_bag(self):
        ...

    # gets the player's active pokemon
    def getActivePokemon(self):
        return self.active_pokemon

    def getAlivePokemonsFromTeam(self, team_name="active"):
        if team_name == "active":
            return self.active_team.alive_pokemons
        else:
            for team in self.teams:
                if team.name == team_name:
                    return team.alive_pokemons

    def getPokemonsFromTeam(self, team_name="active"):
        if team_name == "active":
            return self.active_team.pokemons
        else:
            for team in self.teams:
                if team.name == team_name:
                    return team.pokemons

    def updateAlivePokemonsFromTeam(self, value, team_name="active"):
        if team_name == "active":
            self.active_team.alive_pokemons += value
        else:
            for team in self.teams:
                if team.name == team_name:
                    team.alive_pokemons += value

    # method responsible for checking the users input and set the player's action, if it's valid
    def setAction(self):
        while True:
            actions = ["bag", "pokemons"] + self.getActivePokemon().getMoves(str=True)
            action = input(f"What to do now, {self.nickname}?.. ").lower()
            if action not in actions:
                print("Invalid action")
                continue
            noPP = False
            for move in self.getActivePokemon().getMoves():
                if move.name == action and move.getPP() == 0:
                    print("This movement is out of PP..")
                    noPP = True
            if noPP:
                continue
            self.action = action
            break

    def setTeam(self):
        while True:
            selected_team = input("Select your team, or 'new' for a new team.. ")
            for team in self.teams:
                if selected_team == team.name:
                    return team
            if selected_team == "new":
                while True:
                    team_name = input("Insert your team's name: ")
                    if team_name:
                        for team in self.teams:
                            if team.name == team_name:
                                print(f"There's already a team named {team_name}..")
                                continue
                        break
                self.teams.append(Team.create_team(team_name))
                return

    def save(self, filename, path=PROFILES_PATH):
        path += filename
        with open(path, 'wb') as file:
            pickle.dump(self, file)

    # Creates a new player
    @classmethod
    def create_player(cls):
        # asks for a valid nickname
        while True:
            if nickname:= input("Insert your nickname: "):
                break
        teams = []
        while True:
            team_name = input("Insert your team's name: ")
            if team_name:
                break
        teams.append(Team.create_team(team_name, nickname))
        bag = []
        return cls(nickname, teams, bag)

    @classmethod
    def load_profile(cls, profile, path=PROFILES_PATH):
        path += profile
        try:
            with open(path, "rb") as file:
                player = pickle.load(file)
        except FileNotFoundError:
            print("This profile does not exist")
        else:
            return player