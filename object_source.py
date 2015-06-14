
__author__ = "David Vaillant"

class Inventory():
    """ Keeps track of items in player's possession.
    
    Allows for more detailed collections, including tracking weight and 
    multiple disjoint containers held by the player. """

    def __init__(self, default = {"main":set()}, limits = {"main":-1}):
        ''' Allows for a non-empty initial inventory. '''
        self.holding = default
        self.containers = default.keys()
        self.limits = limits
        self.name = "player inventory"
        
    def add_item(self, x, target="main"):
        ''' Used to add items to the inventory. '''
        ##if self.limits[target] >= x.weight or self.limits[target] == -1:
        ##    return "FULL"
        ##else: pass
        self.holding[target].add(x)
        
        return
        
    def remove_item(self, x, target="main"):
        ''' Used to remove items from the inventory. '''
        try:
            self.holding[target].remove(x)
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
        if not self.holding["main"]:
            return "You are not holding anything."
        for x in self.holding["main"]:
            out_str += x.name + '\n'
        return out_str

class Thing():
    """ Class used to represent items or props.
        ITEMS: Can be placed in player inventory and used from there.
        PROPS: Cannot be moved from their position in a room. """
    codes = {
        '#IDEN':'id',
        '#NAME':'name',
        '#EXMN':'examine_desc',
        '#ONAQ':'on_acquire',
        '#TYPE':'type',
        '#ALIA':'alias',
        '#GRND':'ground_desc',
        '#PROP':'properties',
        '#WGHT':'weight'
        }


    def __init__(self, itemD):
        """ Populates attributes using a Thing info dictionary. """
        
        t = lambda s: itemD[s] if s in itemD.keys() else ''
        self.id = t('IDEN')
        self.name = t('NAME')
        
        self.alias = t('ALIA') or t('NAME') or 'thing'        
        self.properties = t('PROP').split()
        self.weight = t('WGHT') or 0
        self.isProp = t('TYPE') == 'prop'  
        
        self.examine_desc = t('EXMN')
        self.ground_desc = t('GRND')
        
        self.on_acquire = t('ONAQ') or 'pass'


    # NOTE: Need to figure out how to do attribute changes. 
    """
    def safety(self, attributeType, source):
        # Used when changing Thing attributes.
        if type(source) == str: valve = '' 
        elif type(source) == dict: valve = {}

        if attributeType in source.keys():
           return x
        else:
            return valve
    """
    
    def thing_printer(holds):
        out_str = ''
        if holds:
            for x in holds:
                if x.ground_desc == 'pass':
                    pass
                elif x.ground_desc == 'default':
                    out_str = out_str + "\nThere is a " + x.alias + " here."
                else:
                    out_str = out_str + "\n" + x.ground_desc
            return out_str
        else: return ''    
    
    @staticmethod
    def thing_processor(thing_dict):
        """ Returns a Thing class dictionary using a Thing info dictionary. """
        things = {}
        ##thing_dict = thing_fixer(thing_dict)
         
        # iterates over 
        ##for t in thing_dict.values():
        ##    x = Thing(t)
        ##    key = x.id
        ##    things[key] = x
        return {x:Thing(thing_dict[x]) for x in thing_dict}
        
    """
    def thing_fixer(input_dict):
        sourceList = obj_reader(fileIn) if type(fileIn) is str else fileIn
        for ele in input_dict:
            for code in Thing.codes:
                if code[1:] not in ele.keys():
                    ele[code[1:]] = {} if code == '#AC' \
                                    else 'pass'
        return fixed_dict
    """