V = False

class Inventory():
    """ Keeps track of items in player's possession.
    
    Implements weight as well. Eventually... """

    def __init__(self, default = OrdDict({"main":set()}), limits = {"main":-1}):
        """ Allows for a non-empty initial inventory. """
        self.holding = default
        
        self.updateHoldingList()
        
        #self.containers = default.keys()
        self.limits = limits
        self.name = "player inventory"
 
    def __contains__(self, item):
        """ Defines items being "in" Inventory instances. """
        for x in self.holding.values():
            if item in x: return True
        else: return False
        ##return item in self.holding                
    
    def __bool__(self):
        """ Returns True if something is being held. """
        for x in self.holding.values():
            if bool(x): return True
        else: return False
        
    def updateHoldingList(self):
        """ 'Flattens' holding into a cached sum of held items. """
        self.holding_list = []
        for x in self.holding.values():
            if V:
                print(x)
                print(self.holding_list)
            self.holding_list.extend(list(x))
            
    def add(self, x, target="main"):
        """ Adds items to holding[target]. """
        ## TODO: Implement weight.
        ##if self.limits[target] >= x.weight or self.limits[target] == -1:
        ##    return "FULL"
        ##else: pass
        self.holding[target].add(x)
        self.updateHoldingList()
        return
        
    def remove(self, x, target="main"):
        """ Used to remove items from the inventory. """
        ## TODO: Implement weight.
        if target is None:
            target = self.isIn(x)
        if target:
            try:
                self.holding[target].remove(x)
                self.updateHoldingList()
            except KeyError:
                print("WARNING: Something went wrong.")
        return
        
    def isIn(self, x, target="all"):
        """ If x is in a bag, returns the bag. Otherwise, returns None. """
        if target == "all":
            for bag_name, bag in self.holding:
                if x in bag: return bag_name
        return None
        
        
    def __str__(self):
        if not self:
            return "You are not holding anything."
        elif len(self.holding) == 1:
            out_str = 'You are holding:\n'
            for x in self.holding_list:
                out_str += '\t' + x.name + '\n'
        else:
            out_str = "Inventory contents:\n"
            for bag_name, bag in self.holding.items():
                out_str += '\t' + bag_name + '\n'
                if bag:
                    for x in bag: out_str += '\t\t' + x.name + '\n'
                else:
                    out_str += '\t\t' + "Empty!\n"
        return out_str
