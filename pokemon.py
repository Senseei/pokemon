from classes import Battle, Player, Move, Pokemon
import requests

def main():
    # create an empty list of pokemons
    team1 = []

    # get the pichu info and set its moves for tests
    pokemon1info = requests.get("https://pokeapi.co/api/v2/pokemon/pichu").json()
    moves = {}
    move1info = requests.get("https://pokeapi.co/api/v2/move/84").json()
    moves[move1info["name"]] = Move(move1info)
    move2info = requests.get("https://pokeapi.co/api/v2/move/85").json()
    moves[move2info["name"]] = Move(move2info)
    move3info = requests.get("https://pokeapi.co/api/v2/move/86").json()
    moves[move3info["name"]] = Move(move3info)
    move4info = requests.get("https://pokeapi.co/api/v2/move/87").json()
    moves[move4info["name"]] = Move(move4info)
    level = 30
    pokemon1info.update({"level": level, "current_moves": moves})
    # creates the pokemon
    pokemon1 = Pokemon(pokemon1info)
    # append to the list
    team1.append(pokemon1)

    # finally creates the player with the team
    player1 = Player("Sensei", team1)

    # prints the player's pokemons
    print(player1.list_pokemons("stats"))

    # do the same thing but with charmander to the second player
    team2 = []

    pokemon2info = requests.get("https://pokeapi.co/api/v2/pokemon/charmander").json()
    moves = {}
    move1info = requests.get("https://pokeapi.co/api/v2/move/7").json()
    moves[move1info["name"]] = Move(move1info)
    move2info = requests.get("https://pokeapi.co/api/v2/move/34").json()
    moves[move2info["name"]] = Move(move2info)
    move3info = requests.get("https://pokeapi.co/api/v2/move/36").json()
    moves[move3info["name"]] = Move(move3info)
    move4info = requests.get("https://pokeapi.co/api/v2/move/43").json()
    moves[move4info["name"]] = Move(move4info)
    level = 30
    pokemon2info.update({"level": level, "current_moves": moves})
    pokemon2 = Pokemon(pokemon2info)
    team2.append(pokemon2)

    player2 = Player("Lefty", team2)
    print(player2.list_pokemons("battle"))

    # calls a battle and associates it to a variable
    battle = Battle.start_battle(player1, player2)

if __name__ == "__main__":
    main()