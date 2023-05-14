import os.path
import pickle
import time
from datetime import datetime, timedelta
from scripts.utils import strfdelta
from scripts.planes import *


class Stats:
    def __init__(self):
        print("Loading Stats...")
        if not os.path.exists("User Data"):
            os.mkdir("User Data")
        if not os.path.exists("User Data/stats"):
            self.data = {
                "coins": 0,
                "gems": 100,
                "ingame_coins": 0,
                "dogtags": 100,
                "dogtags_timestamp": round(time.time()),
                "selected_plane": F_86_Sabre
            }
            pickle.dump(self.data, open("User Data/stats", "wb"))
        else:
            self.data = pickle.load(open("User Data/stats", "rb"))
        self.dogtags_cooldown = 180
        self.dogtags_limit = 100
        self.dogtags_full = self.data["dogtags"] >= self.dogtags_limit
        print("Stats loaded")
        print(self.data)

    def save(self):
        if not os.path.exists("User Data"):
            os.mkdir("User Data")
        self.data["ingame_coins"] = 0
        pickle.dump(self.data, open("User Data/stats", "wb"))

    def get_plane(self):
        return self.data["selected_plane"]

    def set_plane(self, new_plane):
        self.data["selected_plane"] = new_plane

    def update_dogtags(self):
        self.dogtags_full = self.data["dogtags"] >= self.dogtags_limit
        if self.data["dogtags"] >= self.dogtags_limit:
            self.data["dogtags_timestamp"] = round(time.time())
        else:
            current_time = round(time.time())
            if int((current_time - self.data["dogtags_timestamp"]) / self.dogtags_cooldown) >= 1:
                add_ammount = (current_time - self.data["dogtags_timestamp"]) / self.dogtags_cooldown
                self.data["dogtags"] += int(add_ammount)
                self.data["dogtags"] = min(self.data["dogtags"], self.dogtags_limit)
                self.data["dogtags_timestamp"] = round(time.time())

    def get_next_dogtag_time(self):
        if self.data["dogtags"] < self.dogtags_limit:
            current_time = datetime.fromtimestamp(round(time.time()))
            elapsed = current_time - datetime.fromtimestamp(self.data["dogtags_timestamp"])
            till_next = timedelta(seconds=self.dogtags_cooldown) - elapsed
            return strfdelta(till_next, "{minutes}:{seconds}")
        else:
            return strfdelta(timedelta(seconds=self.dogtags_cooldown), "{minutes}:{seconds}")

    def add_coins(self, amount):
        self.data["coins"] += amount

    def add_ingame_coins(self, amount):
        self.data["ingame_coins"] += amount

    def can_purchase(self, currency, cost):
        if self.data[currency] >= cost:
            return True
        return False
