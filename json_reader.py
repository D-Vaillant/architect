import json
from rooms import Room
from item import Item
from inventory import Inventory
from actions import Action
from collections import OrderedDict as OrdDict

class InfoCollector:
    def __init__(self):
        self.action_info = {}
        self.item_info = {}
        self.room_info = {}

    def main(self):
        with open("desc_test.json", 'r') as F:
            p = json.load(F)
        
        for x in p:
            getattr(self, x["type"]+"_info").update({x["id"]:x})
        return
