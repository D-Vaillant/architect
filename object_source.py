
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
        #if self.limits[target] >= x.weight or self.limits[target] == -1:
        #    return "FULL"
        #else: pass
        self.holding[target].add(x)
        
        return
        
    def remove_item(self, x, target="main"):
        ''' Used to remove items from the inventory. '''
        try:
            self.holding[target].remove(x)
        except KeyError:
            print("WARNING: Something went wrong.")
        return
        
    def __str__(self):
        out_str = 'You are holding:\n'
        if not self.holding["main"]:
            return "You are not holding anything."
        for x in self.holding["main"]:
            out_str += x + '\n'
        return out_str

class Thing():
    """ Class used to represent items or props.
        ITEMS: Can be placed in player inventory and used from there.
        PROPS: Cannot be moved from their position in a room. """
    codes = {
        '#NA':'name',
        '#EX':'examine_desc',
        '#OA':'on_acquire',
        '#AC':'action',
        '#TY':'type',
        '#AL':'alias',
        '#GD':'ground_desc',
        '#PR':'properties',
        '#WT':'weight'
        }


    def __init__(self, itemD):
        """ Populates attributes using a Thing info dictionary. """
        
        self.name = itemD['NA'] if 'NA' in itemD.keys() else ''
        
        self.alias = itemD['AL'] if 'AL' in itemD.keys() else 'thing'        
        self.properties = itemD['PR'].split() if 'PR' in itemD.keys() else ''
        self.weight = itemD['WT'] if 'WT' in itemD.keys() else 0
        self.isProp = True if itemD['TY'] == 'prop' else False   
        
        self.examine_desc = itemD['EX'] if 'EX' in itemD.keys() else ''
        self.ground_desc = itemD['GD'] if 'GD' in itemD.keys() else ''
        
        self.on_acquire = itemD['OA'] if 'OA' in itemD.keys() else 'pass'
        self.action_dict = {act:mcode for act, mcode in itemD['AC'].items()} \
                            if 'AC' in itemD.keys() else {}


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
            
    def thing_processor(thing_dict):
        """ Returns a Thing class dictionary using a Thing info dictionary. """
        things = {}
        #thing_dict = thing_fixer(thing_dict)
         
        # iterates over 
        for j in thing_dict:
            x = Thing(thing_dict[j])
            key = x.alias
            things[key] = x
        return things
        
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