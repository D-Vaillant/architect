__author__ = "David Vaillant"

class Inventory():
    def __init__(self):
        self.collection = {}
        
    def add_item(self, x):
        if x not in self.collection.keys():
            self.collection[x] = 1
        else:
            self.collection[x] += 1
        return
        
    def remove_item(self, x):
        if x in self.collection.keys():
            self.collection[x] = max(x-1, 0)
        else:
            print("Warning: Trying to remove a non-existent object.")
            return
            
class Item():
    def __init__(self, itemD):
        self.name = itemD[NA]
        self.examine_desc = itemD[EX] if itemD[EX] != None else 'N/A'
        self.machine_code = ''
       
        
        