""" ontology.py
        Defines the various implementations of "concrete objects" used in
    Architect-based games. """

__author__ = "David Vaillant"

from collections import OrderedDict as OrdDict

verbose = False
careful = False

class Inventory():
    """ Keeps track of items in an Actor's possession.
    
    Implements weight as well. Eventually... """

    def __init__(self, contents = None, limits = None):
        """ Allows for a non-empty initial inventory. """
        if contents is None:
            self.holding = OrdDict({"main":set()})
        else:
            self.holding = contents

        if limits is None:
            self.capacities = {x:-1 for x in self.holding}
        else:
            self.capacities = limits
        
        #self.updateHoldingList()
        
        self.name = "Generic Inventory"
 
    def __getitem__(self, bag_name):
        try:
            return self.holding[bag_name]
        except KeyError:
            raise KeyError("No bag with that name.")

    def __contains__(self, item):
        """ Defines items being "in" Inventory instances. """
        return any(item in bag for bag in self.holding.values())
    
    def __bool__(self):
        """ Returns True if something is being held. """
        #for x in self.holding.values():
        #    if bool(x): return True
        #else: return False
        return any(self.holding.values())
        
    def _canHold(self, bag, item):
        if self.capacities[bag] < 0: return True 

        return self.capacities[bag] >= item.weight

    '''
    def updateHoldingList(self):
        """ 'Flattens' holding into a cached sum of held items. """
        self.holding_list = []
        for x in self.holding.values():
            if verbose:
                print(x)
                print(self.holding_list)
            self.holding_list.extend(list(x))
   '''

    def add(self, x, target = None):
        """ Adds items to holding[target]. """
        ## TODO: Implement weight.
        if target is None:
            for bag_name, bag in self.holding.items():
                if self._canHold(bag_name, x): 
                    target = bag_name
                    break

        try:
            self[target].add(x)
            return 0
        except KeyError:
            if target is None:
                return -1
            else:
                raise KeyError("Tried to add to a non-existent bag, {}.".format(bag_name))
        
    def remove(self, x, target="main"):
        """ Used to remove items from the inventory. """
        ## TODO: Implement weight.
        if target is None:
            target = self.find(x)
        if target:
            try:
                self[target].remove(x)
                #self.updateHoldingList()
            except KeyError:
                print("WARNING: Something went wrong.")
        return
        
    def find(self, x):
        """ If x is in a bag, returns the bag. Otherwise, returns None. """
        for bag_name, bag in self.holding:
            if x in bag: return bag_name
        return None
        
    def __iter__(self):
        for bag in self.holding.values():
            for item in bag:
                yield item

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
        self.id = itemD.get("id")
        self.name = itemD.get("name")
        
        self.nickname = itemD.get("nick") or itemD.get("name", "item")

        self.properties = set(itemD.get('property', {}))
        self.weight = itemD.get("weight", 0)
        self.isProp = ("static" in self.properties)  

        self.examine_desc = itemD.get("examine", '')
        self.ground_desc = itemD.get("ground", '')

        # BP code to be run when an Item is picked up
        # Probably better to make this into an Event.
        self.on_acquire = itemD.get("acquire", "pass")

    def is_(self, property_):
        return property_ in self.properties

    def setProperty(self, property_input, isAdding = True):
        """ Adds or removes a property from an Item. """
        if isAdding:
            self.properties.add(property_input)
            return False
        else:
            try:
                self.properties.remove(property_input)
                return False
            except KeyError:
                return True

    def setDescription(self, type, text = ""):
        """ Changes type_desc attribute to specified text. """
        if hasattr(self, type+"_desc"):
            setattr(self, type+"_desc", text)
            return False
        else: 
            return True

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

class Room():
    """ Room class. """
    codes = {
        'id':'id',
        'name':'name',
        'desc':'entry_desc',
        'hold':'holding',
        'links':'links'
            }
        
    def __init__(self, roomD):
        self.id_ = roomD.get("id") 

        self.links = roomD.get("links", [None,None,None,None])
        self.name = roomD.get("name", '')
        
        dsc = roomD.get("desc")
        # Used to catch lazy setting single-line descriptions
        # as strings instead of singleton lists.
        self.entry_desc = [dsc] if isinstance(dsc, str) else (dsc or 
                                                          ["This is a room."])
           
        self.holding = roomD.get("hold", [])
        # Used to catch setting holding to a string instead of a list.
        if isinstance(self.holding, str): 
            self.holding = [self.holding]

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
                                               self.id_,
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

class Action():
    """ The backbone of action functions. Weird. """
    prep = None 
    #id_ = None

    def __init__(act, Engine, args = None):
        """Passes access to the Engine, gives arguments.""" 
        # Gives the Action a handle on the Engine.
        # The relation is interesting and subtle. We want actions to be
        #   able to do what bp_parser is doing: execute some simple commands.
        #   The Engine might instead be a submodule of Game.
        act.E = Engine
        act.nullary = args is None
        # a goofy way to ensure that only pairs count as binary
        try:
            act.binary = True if len(args) == 2 else False
            act.unary = not act.binary
        except TypeError:
            act.unary = not act.nullary
            act.binary = False

        if act.unary: assert isinstance(args, Item) 
        elif act.binary:
            for _ in args: assert isinstance(_, Item)

        act.call(args)

    def call(act, args):
        """The structure of an Action call."""
        if act.nullary:
            act.zero()
        elif act.unary:
            act.one(args)
        elif act.binary:
            act.two(*args)
        else:
            raise Exception("Invalid branch.")

    def zero(act):
        pass

    def one(act, arg):
        pass

    def two(act, arg0, arg1):
        E.err("Input > Max")

class Actor:
    """ Parent class for any Player-esque character. """
    def __init__(self, id_,
                       name = "Nameless",
                       max_health = -1,
                       attributes = {},
                       carrying = None):
        self.iden = id_
        self.name = name
        self.max_health = max_health
        self.health = self.max_health

    def harm(self, dmg):
        """Hurts the Actor for `dmg` points."""
        if self.health < 0:
            pass # negative health = immune to damage!
        elif self.health < dmg:
            self.die()
        else:
            self.health -= dmg

    def die(self):
        pass

        # carrying is either a single item or an array of items

# not imported so no need to do much here
class OldAction:
    codes = {
        "id":   "id",
        "zero": "zero_act",
        "one":  "unary_act",
        "two":  "binary_act",
        "prep": "binary_prep"
        }

    def __init__(self, actionD):
        self.id = actionD.get("id") 

        self.zero_act = actionD.get("zero", "pass").split('&')
        self.unary_act = self.unaryHelper(actionD.get("one", {'':"pass"}))
        self.binary_act = self.binaryHelper(actionD.get("two", {'|':"pass"}))
        self.binary_prep = actionD.get("prep", "")

        self.min, self.max = self.min_maxHelper()
        self.isKnown = actionD.get("isKnown", True)

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
