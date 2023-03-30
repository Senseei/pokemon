import random

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
            self.current_stat = self.stat * (1 + self.stat_level / 2)
        else:
            self.current_stat = self.stat * negative_stat_level_table[self.stat_level]

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