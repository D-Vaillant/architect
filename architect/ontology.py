""" ontology.py
        Defines the various implementations of "concrete objects" used in
    Architect-based games. """

__author__ = "David Vaillant"

from collections import OrderedDict as OrdDict

verbose = False
careful = False

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
    
    def __bool__(self):
        """ Returns True if something is being held. """
        for x in self.holding.values():
            if bool(x): return True
        else: return False
        
    def updateHoldingList(self):
        """ 'Flattens' holding into a cached sum of held items. """
        self.holding_list = []
        for x in self.holding.values():
            if verbose:
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

class Item():
    """ Class used to represent items or props.
        ITEMS: Can be placed in player inventory and used from there.
        PROPS: Cannot be moved from their position in a room. """
    codes = {
        'id':'id',
        'name':'name',
        'nick':'nickname',
        'examine':'examine_desc',
        'acquire':'on_acquire',
        'ground':'ground_desc',
        'property':'properties',
        'weight':'weight'
        }


    def __init__(self, itemD):
        """ Populates attributes using a Item info dictionary. """
        t = lambda s: itemD[s] if s in itemD.keys() else None
        
        self.id = t('id')
        self.name = t('name')
        
        self.nickname = t('nick') or t('name') or 'item'                
        self.properties = set(t('property') or {})
        self.weight = t('weight') or 0
        self.isProp = ('static' in self.properties)  
        
        self.examine_desc = t('examine') or ''
        self.ground_desc = t('ground') or ''
        
        self.on_acquire = t('acquire') or 'pass'

    def setProperty(self, property_input, isAdding = True):
        error = False
        
        if isAdding:
            self.properties.add(property_input)
        else:
            try:
                self.properties.remove(property_input)
            except KeyError: error = True
        return error #if setProperty: error handle.

    def setDescription(self, type, text = ""):
        error = False
        
        if hasattr(self, type+"_desc"):
            setattr(self, type+"_desc", text)
        else:
            error = True #if setDescription: error handle.
        return error

    ### NOTE: This could probably be moved elsewhere. ###
    ### Related: __str__ method for Items. ###
    @staticmethod
    def item_printer(holds):
        out_str = ''
        if holds:
            for x in holds:
                if x.ground_desc == 'pass':
                    pass
                elif x.ground_desc == 'default':
                    out_str = out_str + "\nThere is a " + x.name + " here."
                else:
                    out_str = out_str + "\n" + x.ground_desc
            return out_str
        else: return ''    
    
    @staticmethod
    def item_processor(item_dict):
        """ Returns a Item class dictionary using a Item info dictionary. """
        return {x:Item(item_dict[x]) for x in item_dict}

class Room():
    """ Room class. """
    codes = {
        'id':'id',
        'name':'name',
        'desc':'entry_desc',
        'hold':'holding',
        'links':'links'
            }
        
    def __init__(self, r):
        d = lambda s: r[s] if s in r else None

        self.id = d('id') 

        self.links = d('links') or [None]*4
        self.name = d('name') or ''
        
        _ = d('desc')
        if type(_) == str:
            self.entry_desc = [_]
        else:
            self.entry_desc = _ or ["This is a room."]
           
        self.holding = d('hold') or []
        # Used to catch lazy settings of holding to a string instead of a list.
        if type(self.holding) == 'str': self.holding = [self.holding]
        ##if d('data'): self.data = []

        self.is_visited = False
        
    def __contains__(self, item):
        """ Simplifies 'in' calls. """
        return item in self.holding
            
    def add(self, item):
        self.holding.append(item)
        
    def remove(self, item):
        self.holding.remove(item)
        
    def onEntry(self):
        """ Runs whenever a room is entered. """
        self.is_visited = True
        out = "\n".join(self.entry_desc)
        return out
        
    def link(self, linked_room, dir, isEuclidean = True):
        if isEuclidean and self == linked_room:
            raise TypeError("Euclidean rooms enabled; no loops allowed.")

        self.links[dir] = linked_room
        if isEuclidean:
            if dir == 0: dir = 3
            elif dir == 1: dir = 2
            elif dir == 2: dir = 1
            elif dir == 3: dir = 0
            linked_room.links[dir] = self
 
    def __str__(self):  
        string = ("Name: {0}\n"
                  "ID: {1}\n"
                  "Entry message: {2}\n"
                  "Items contained: [").format(self.name,
                                               self.id,
                                               self.entry_desc)        
        for x in self.holding:
            try:
                string += x.id + " "
            except AttributeError:
                try:
                    string += x + " "
                except TypeError:
                    string += "ERROR: ABNORMAL HOLDINGS"
        string += "] \n"
        
        return string  
        
    @staticmethod
    def room_processor(room_info_dict):
        """ Takes a Room info dictionary and creates a Room class dictionary.

        If a link info dictionary is provided, runs each Room's
        link_processor method to set the attribute. """
        r = {}
        # Iterates through the dictionary's keys and creates a new Room using
        # the associated value (a Room info dictionary).
        for x in room_info_dict:
            r[x] = Room(room_info_dict[x])
        return r

class Action:
    codes = {
        "id":   "id",
        "zero": "zero_act",
        "one":  "unary_act",
        "two":  "binary_act",
        "prep": "binary_prep"
        }

    def __init__(self, id,
                       zero =   'pass',
                       one =    {'' : 'pass'},
                       two =    {'|': 'pass'},
                       prep =    '',
                       isKnown = True,
                       **kwargs):
        self.id = id

        self.zero_act = zero.split('&')
        self.unary_act = self.unaryHelper(one)
        self.binary_act = self.binaryHelper(two)
        self.binary_prep = prep

        self.min, self.max = self.min_maxHelper()
        self.isKnown = isKnown

    def unaryHelper(self, act_list):
        """ Takes a list of lists of length 2, produces an OrderedDict. """
        K = lambda x: tuple(x.split('&'))
        V = lambda y: y if type(y) is list else y.split('&')

        return OrdDict((K(x),V(y)) for x, y in act_list.items())

    def binaryHelper(self, act_list):
        """ Takes a list of lists of length 2, produces an OrderedDict. """
        def K(k):
            if '|' not in k:
                if careful: 
                    raise SyntaxError("Binary conditional key missing |.")
                else:
                    k = k + '|'
            k = k.split('|')
            for index, val in enumerate(k):
                k[index] = tuple(val.split('&'))
            return tuple(k)

        V = lambda y: y if type(y) is list else y.split('&')

        return OrdDict((K(x),V(y)) for x, y in act_list.items())

    def min_maxHelper(self):
        min, max = None, None

        if self.zero_act != ['pass']:
            min = 0
            max = 0
        if self.unary_act != {'':['pass']}:
            if min is None: min = 1
            max = 1
        if self.binary_act != {('',''):['pass']}:
            if min is None: min = 2
            max = 2

        if min is None: min = -1
        if max is None: max = -1
        return min, max

    @staticmethod
    def unaryTest(item, condition):
        """ Tests if item fulfills the given condition. """
        if verbose: print("Testing condition: {}".format(condition))
    
        # Skip evaluation if empty condition is given.
        if condition == '': return True

        is_negated = (condition[0] == '~')
        if is_negated: condition = condition[1:] 

        if condition[:2] == 'p:':
            val = (condition[2:] in item.properties)
        else:
            val = (condition == item.id)
        return (not val) if is_negated else val
    
    @staticmethod
    def pluralUnaryTest(single_obj, condition_array):
        for x in condition_array:
            if Action.unaryTest(single_obj, x): continue 
            else: return False
        return True

    def call(self, input_objs):
        """ Takes either an Item or a tuple or Items, returns BP code. """
        val = None
        if input_objs == 0:
            val = self.zero_act

        elif(len(input_objs) == 2):
            for (i,j),bp in self.binary_act.items():
                if self.pluralUnaryTest(input_objs[0], i) and \
                   self.pluralUnaryTest(input_objs[1], j):
                        val = bp 
                        break
                else: continue

        else: # Only one object.
            for i,bp in self.unary_act.items():
                if self.pluralUnaryTest(input_objs[0], i):
                    val = bp 
                    break
                else: continue

        if verbose: print("Returning {}.".format(val))
        return val or 'pass'

    @staticmethod
    def action_processor(action_dict):
        """ ugh """
        actions = {}

        for i,j in action_dict.items():
            actions[i] = Action(**j)
        return actions

class Actor:
    """ Parent class for any Player-esque character. """
    def __init__(self, id,
                       name = "Nameless",
                       health = None,
                       attributes = {},
                       carrying = None):
        self.id = id
        self.name = name
        self.health = health

class Player(Actor):
    def __init__(self, id, **kwargs):
        self.super().__init__(id, kwargs)
