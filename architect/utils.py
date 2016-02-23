import json
import re

from collections import OrderedDict as OrdDict
from pyparsing import oneOf, Optional, Literal
from pyparsing import StringEnd, Or, Empty, SkipTo, ParseException 

class Parser:
    def __init__(self, r, i, a, b):
        """ Takes information from Game class to initialize parsing. """

        self.rooms = r
        self.items = i
        self.actions = a
        self.inventory = b

        self.bp_commands = ['puts', 'link', 'add', 'remove', 'move',
                            'changeRoom', 'changeItem', 'changeInventory',
                            'addProperty', 'removeProperty',
                           ]
        
    def bpParse(self, code):
        """ Given a line of BP code, parses out the command and parameters. 
        INPUT: "CMD(ARGS)" => OUTPUT: CMD, [ARG_0..ARG_n] """
        if code=='pass': return code

        """
        j = lambda x: ' '.join(x)
        item = oneOf(j(self.items.keys())) # string of all the item names
        item_attr = oneOf("name nick weight ground_desc examine_desc")

        room = oneOf(j(self.rooms.keys())) # string of all the room names
        room_attr = oneOf("name")
        dir = oneOf("W S N E")
        # string of all the names of different bags

        bag = oneOf(j(self.inventory.holding.keys()))
        bag_attr = oneOf("add remove limit")
        container = ('_' ^ room) + Optional(Literal('.') + bag)

        rest = SkipTo(StringEnd())
        change = lambda x,y: x + '.' + y + '=' + rest

        # hash associating commands with their calling syntax
        # all syntax has the form ARG SYM ARG SYM ARG SYM..., to allow for
        # symbols to be easily ignored when passing parsed results
        pt = {
                'puts' : rest,
                'link': room + '-' + dir + '->' + room,
                'add': item + '@' + container,
                'remove': item + '@' + container,
                'move': item + '@' + container + '->' + container,
                'changeItem': change(item, item_attr),
                'changeRoom': change(room, room_attr),
                'changeInv': change(bag, bag_attr),
                'addProperty': item + '#' + rest,
                'removeProperty': item + '#' + rest,
             }
        """
        
        # Finds the first instance of !; used to divide CMD from PARAMS.
        argumentRegex = "([A-Za-z0-9, ]+)"
        functionRegex = "(\w+)" + "\(" + argumentRegex + "\)"
        _ = re.search(functionRegex, code)
        command = _.group(1)
        parameters = [x.strip() for x in _.group(2).split(',')]
        
        """
        try:
            return command, pt[command].parseString(parameters)[::2]
        except KeyError:
            raise KeyError("Attempted to call the %s command."%command)
        """
        return command, parameters
        
    def actionParse(self, Act, parameters):
        """ Parses arity and item IDs from a user action command. """
        item_names_list = [_.name for _ in self.items.values()] +\
               [_.nickname for _ in self.items.values()]
        item = oneOf(' '.join(item_names_list))
        
        zero = Empty()
        first = item
        second = Literal(Act.binary_prep) + item if Act.binary_prep\
              else Empty()
        
        out = None 
        if parameters:
            if Act.max > 0:
                if Act.min == 2: _ = first + second
                else: _ = first + Optional(second)
                
                try:
                    out = _.parseString(parameters).asList()[::2]
                except ParseException:
                    out = "$! Input < Min"
            else:
                out = "$! Input > Max"
                
            
        else:
            if Act.min == 0: out = []
            else: out = "$! 0 < Min"
        return out 

class JSON_Reader:
    def __init__(self, filename = "resource_files/desc_test.json"):
        self.f = filename

        self.action_info = {}
        self.item_info = {}
        self.room_info = {}
        self.meta_info = {}
        
        self.main()

    def main(self):
        with open(self.f, 'r') as F:
            p = json.load(F, object_pairs_hook=OrdDict)
        for x in p:
            try:
                getattr(self, x["type"]+"_info").update({x["id"]:x})
            except KeyError:
                raise KeyError("Found an entry without a type or an id. " +
                               "Don't forget those!")
        
    def output(self):
        return (self.room_info, self.item_info, 
                self.action_info, self.meta_info)


