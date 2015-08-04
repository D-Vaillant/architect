V = False

class Inventory():
    """ Keeps track of items in player's possession.
    
    Implements weight as well. Eventually... """

    def __init__(self, default = {"main":set()}, limits = {"main":-1}):
        ''' Allows for a non-empty initial inventory. '''
        self.structured_holding = default
        
        self.update_holding()
        
        self.containers = default.keys()
        self.limits = limits
        self.name = "player inventory"
 
    def __contains__(self, item):
        for x in self.structured_holding.values():
            if item in x: return True
        else: return False
        ##return item in self.holding                
    
    def __bool__(self):
        for x in self.structured_holding.values():
            if bool(x): return True
        else: return False
        
    #! Possibly deprecated by operation redefinitions.
    def update_holding(self):
        """ 'Flattens' structured_holding to easily check for containing. """
        self.holding = []
        for x in self.structured_holding.values():
            if V:
                print(x)
                print(self.holding)
            self.holding.extend(list(x))
            
    def add(self, x, target="main"):
        """ Adds items to structured_holding[target]. """
        ##if self.limits[target] >= x.weight or self.limits[target] == -1:
        ##    return "FULL"
        ##else: pass
        self.structured_holding[target].add(x)
        ##self.update_holding()
        return
        
    def remove(self, x, target="main"):
        ''' Used to remove items from the inventory. '''
        try:
            self.structured_holding[target].remove(x)
            ##self.update_holding()
        except KeyError:
            print("WARNING: Something went wrong.")
        return
        
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
