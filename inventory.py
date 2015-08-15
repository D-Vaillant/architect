V = False

class Inventory():
    """ Keeps track of items in player's possession.
    
    Implements weight as well. Eventually... """

    def __init__(self, default = {"main":set()}, limits = {"main":-1}):
        """ Allows for a non-empty initial inventory. """
        self.holding = default
        
        self.updateHoldingList()
        
        self.containers = default.keys()
        self.limits = limits
        self.name = "player inventory"
 
    def __contains__(self, item):
        """ Defines items being "in" Inventory instances. """
        for x in self.structured_holding.values():
            if item in x: return True
        else: return False
        ##return item in self.holding                
    
    def __bool__(self):
        """ Returns True if something is being held. """
        for x in self.structured_holding.values():
            if bool(x): return True
        else: return False
        
    def updateHoldingList(self):
        """ 'Flattens' holding into a cached sum of held items. """
        self.holding_list = []
        for x in self.structured_holding.values():
            if V:
                print(x)
                print(self.holding_list)
            self.holding_list.extend(list(x))
            
    def add(self, x, target="main"):
        """ Adds items to structured_holding[target]. """
        ## TODO: Implement weight.
        ##if self.limits[target] >= x.weight or self.limits[target] == -1:
        ##    return "FULL"
        ##else: pass
        self.structured_holding[target].add(x)
        self.updateHoldingList()
        return
        
    def remove(self, x, target="main"):
        """ Used to remove items from the inventory. """
        ## TODO: Implement weight.
        try:
            self.structured_holding[target].remove(x)
            self.updateHoldingList()
        except KeyError:
            print("WARNING: Something went wrong.")
        return
        
    ## TODO: Figure out where this plays in.
    def isIn(self, x, target="all"):
        """ Returns True if x is in target. Defaults to checking all. """
        for pouch in self.containers:
            if x in pouch: return True
        return False
        
        
    def __str__(self):
        out_str = 'You are holding:\n'
        if not self.holding:
            return "You are not holding anything."
        for x in self.holding:
            out_str += x.name + '\n'
        return out_str
