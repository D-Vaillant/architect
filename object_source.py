
__author__ = "David Vaillant"

class Inventory():
    ''' A rudimentary clone of the Counter class. Used to represent a player's
        inventory. '''

    def __init__(self, default = {}):
        ''' Allows for a non-empty initial inventory. '''
        self.holding = default
        
    def add_item(self, x):
        ''' Used to add items to the inventory. '''
        try:
            self.holding[x] += 1
        except KeyError:
            self.holding[x] = 1
        return
        
    def remove_item(self, x):
        ''' Used to remove items from the inventory. '''
        if x in self.holding.keys():
            self.holding[x] = max(x-1, 0)
        else:
            print("Warning: Trying to remove a non-existent object.")
            return
            
class Thing():
    ''' Class used to represent items or props.
        ITEMS: Can be placed in player inventory and used from there.
        PROPS: Cannot be moved from their position in a room. '''
    codes = {
        '#NA':'name',
        '#EX':'examine_desc',
        '#OA':'on_acquire',
        '#AC':'action',
        '#TY':'type',
        '#AL':'alias',
        '#GD':'ground_desc'
        }


    def __init__(self, itemD):
        """ Populates attributes using a Thing info dictionary. """
        self.name = itemD['NA'] if 'NA' in itemD.keys() else ''
        self.alias = itemD['AL'] if 'AL' in itemD.keys() else 'thing'
        self.examine_desc = itemD['EX'] if 'EX' in itemD.keys() else ''
        self.ground_desc = itemD['GD'] if 'GD' in itemD.keys() else ''
        self.on_acquire = itemD['OA'] if 'OA' in itemD.keys() else 'pass'
        self.action_dict = {act:mcode for act, mcode in itemD['AC'].items()} \
                            if 'AC' in itemD.keys() else {}
        self.isProp = True if itemD['TY'] == 'prop' else False

    # NOTE: Need to figure out how to do attribute changes. 
    def safety(self, attributeType, source):
        """ Used when changing Thing attributes. """
        if type(source) == str: valve = '' 
        elif type(source) == dict: valve = {}

        if attributeType in source.keys():
           return x
        else:
            return valve
    
    def thing_processor(thing_dict):
        """ Returns a Thing class dictionary using a Thing info dictionary. """
        things = dict()
        #thing_dict = thing_fixer(thing_dict)
         
        # iterates over 
        for j in thing_dict:
            x = Thing(thing_dict[j])
            key = x.alias
            things[key] = x
        return things
        
    def thing_fixer(input_dict):
        sourceList = obj_reader(fileIn) if type(fileIn) is str else fileIn
        for ele in input_dict:
            for code in Thing.codes:
                if code[1:] not in ele.keys():
                    ele[code[1:]] = {} if code == '#AC' \
                                    else 'pass'
        return fixed_dict
