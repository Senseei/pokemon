from classes.pokemon import Pokemon

class Team:
    def __init__(self, name, pokemons=[]):
        self.name = name
        self.pokemons = pokemons
        self.alive_pokemons = len(self.pokemons)

    @classmethod
    def create_team(cls, team_name, owner):
        # creates an empty list of pokemons with max length 6
        pokemons = []
        while len(pokemons) < 6:
            try:
                pokemons.append(Pokemon.create_pokemon(owner))
            except EOFError:
                print("\n")
                break
            except:
               continue
        return cls(team_name, pokemons)