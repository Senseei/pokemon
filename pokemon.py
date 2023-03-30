from classes.battle import Battle
from classes.commandline import CommandLine
from classes.player import Player
from classes import PROFILES_PATH
import sys

def main():
    # checks if the arguments are valid
    if not CommandLine.check(sys.argv):
        sys.exit("Usage: python pokemon.py <player1.profile> <player2.profile>")

    # checks if the profiles do exist, if not, it will create a new profile
    if CommandLine.file_exists(PROFILES_PATH + sys.argv[1]):
        player1 = Player.load_profile(PROFILES_PATH + sys.argv[1])
    else:
        player1 = Player.create_player()
        player1.save(PROFILES_PATH + sys.argv[1])
    if CommandLine.file_exists(PROFILES_PATH + sys.argv[2]):
        player2 = Player.load_profile(PROFILES_PATH + sys.argv[2])
    else:
        player2 = Player.create_player()
        player2.save(PROFILES_PATH + sys.argv[2])

    # calls a battle and associates it to a variable
    battle = Battle.start_battle(player1, player2)

if __name__ == "__main__":
    main()