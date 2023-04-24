import os.path
import pickle


class Stats:
    def __init__(self):
        print("Loading Stats...")
        if not os.path.exists("User Data"):
            os.mkdir("User Data")
        if not os.path.exists("User Data/stats"):
            self.data = {
                "coins": 0,
                "gems": 0,
                "ingame_coins": 0,
                "dogtags": 0
            }
            pickle.dump(self.data, open("User Data/stats", "wb"))
        else:
            self.data = pickle.load(open("User Data/stats", "rb"))
        print("Stats loaded")
        print(self.data)

    def save(self):
        if not os.path.exists("User Data"):
            os.mkdir("User Data")
        pickle.dump(self.data, open("User Data/stats", "wb"))

    def add_coins(self, amount):
        self.data["coins"] += amount

    def add_ingame_coins(self, amount):
        self.data["ingame_coins"] += amount

