from classes import Battle, Player, Move, Pokemon, Team
import requests

def main():
    # create an empty list of pokemons
    team1 = []

    # get two pokemons' info and set its moves for tests
    pokemon1info = requests.get("https://pokeapi.co/api/v2/pokemon/garchomp").json()
    moves = {}
    move1info = requests.get("https://pokeapi.co/api/v2/move/earthquake").json()
    moves[move1info["name"]] = Move(move1info)
    level = 100
    pokemon1info.update({"level": level, "current_moves": moves})
    # creates the pokemon
    pokemon1 = Pokemon(pokemon1info)
    # append to the list
    team1.append(pokemon1)

    pokemon1info = requests.get("https://pokeapi.co/api/v2/pokemon/charizard").json()
    moves = {}
    move1info = requests.get("https://pokeapi.co/api/v2/move/flamethrower").json()
    moves[move1info["name"]] = Move(move1info)
    level = 100
    pokemon1info.update({"level": level, "current_moves": moves})
    # creates the pokemon
    pokemon1 = Pokemon(pokemon1info)
    # append to the list
    team1.append(pokemon1)
    # creates a team object
    obj_team1 = Team("team1", team1)
    # finally creates the player with the team
    player1 = Player("Sensei", teams=[obj_team1], bag=[])

    # prints the player's pokemons
    print(player1)

    # do the same thing but with charmander to the second player
    team2 = []

    pokemon2info = requests.get("https://pokeapi.co/api/v2/pokemon/raichu").json()
    moves = {}
    move1info = requests.get("https://pokeapi.co/api/v2/move/thunder").json()
    moves[move1info["name"]] = Move(move1info)
    move2info = requests.get("https://pokeapi.co/api/v2/move/body-slam").json()
    moves[move2info["name"]] = Move(move2info)
    level = 100
    pokemon2info.update({"level": level, "current_moves": moves})
    pokemon2 = Pokemon(pokemon2info)
    team2.append(pokemon2)

    pokemon2info = requests.get("https://pokeapi.co/api/v2/pokemon/dragonite").json()
    moves = {}
    move1info = requests.get("https://pokeapi.co/api/v2/move/thunder").json()
    moves[move1info["name"]] = Move(move1info)
    move2info = requests.get("https://pokeapi.co/api/v2/move/ice-beam").json()
    moves[move2info["name"]] = Move(move2info)
    level = 100
    pokemon2info.update({"level": level, "current_moves": moves})
    pokemon2 = Pokemon(pokemon2info)
    team2.append(pokemon2)

    obj_team2 = Team("team1", team2)

    player2 = Player("Lefty", teams=[obj_team2], bag=[])
    print(player2)

    # calls a battle and associates it to a variable
    battle = Battle.start_battle(player1, player2)

if __name__ == "__main__":
    main()