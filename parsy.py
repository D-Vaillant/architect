from pyparsing import oneOf, Optional, Literal, SkipTo, StringEnd, Or 

class Parser:
    def __init__(self, r, i, a, b):
        """ Takes information from Game class to initialize parsing. """

        self.rooms = r
        self.items = i
        self.actions = a
        self.inventory = b

        self.bp_commands = ['put', 'link', 'add', 'remove', 'move',
                            'changeRoom', 'changeItem', 'changeInventory',
                            'addProperty', 'removeProperty',
                           ]
        
    def bpParse(self, code):
        """ Given a line of BP code, parses out the command and parameters. """

        j = lambda x: ' '.join(x)
        item = oneOf(j(self.items.keys())) # string of all the item names
        item_attr = oneOf("name nick weight ground_desc examine_desc")

        room = oneOf(j(self.rooms.keys())) # string of all the room names
        room_attr = oneOf("name")
        dir = oneOf("W S N E")
        # string of all the names of different bags

        bag = oneOf(j(self.inventory.structured_holding.keys()))
        bag_attr = oneOf("add remove limit")
        container = '_' ^ room + Optional('.' + bag)

        rest = SkipTo(StringEnd())
        change = lambda x,y: x + '.' + y + '=' + rest

        # hash associating commands with their calling syntax
        # all syntax has the form ARG SYM ARG SYM ARG SYM..., to allow for
        # symbols to be easily ignored when passing parsed results
        pt = {
                'put' : rest
                'link': room + '-' + dir + '->' + room,
                'add': item + '@' + container
                'remove': item + '@' + container,
                'move': item + '@' + room + '->' + container
                'changeItem': change(item, item_attr),
                'changeRoom': change(room, room_attr),
                'changeInv': change(bag, bag_attr),
                'addProperty': item + '#' + rest,
                'removeProperty': item + '#' + rest,
             }

        index = code.find('!')
        command = code[:index]
        parameters = code[index+1:]

        return command, pt[command].parseString(parameters)[::2]

    def actionParse(self, Act, parameters):
        """ Parses arity and item IDs from a user action command. """
        j = lambda x: ' '.join(x)
        item = oneOf(j(self.items.keys())) # string of all the item names        
        
        zero = Literal('')
        one = item
        two = Literal(Act.binary_prep) + item
        
        out = None 
        if parameters:
            if Act.max > 0:
                if Act.min == 2: _ = one + two
                else: _ = one + Optional(two)
            else:
                out = "$! Input > Min"
                
            try:
                out = _.parseString(parameters)
            except AttributeError:
                out = "$! Input < Min"
        else:
            if Act.min == 0: out = []
            else: out = "$! 0 < Min"
        return out 