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
        
    def BP_Parse(self, code):
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
        container = '_' ^ room
        rest = SkipTo(StringEnd())

        change = lambda x,y: x + '.' + y + '=' + rest

        # hash associating commands with their calling syntax
        # all syntax has the form ARG SYM ARG SYM ARG SYM..., to allow for
        # symbols to be easily ignored when passing parsed results
        pt = {
                'put' : rest
                'link': room + '-' + dir + '->' + room,
                'add': item + '@' + container + Optional('.' + bag),
                'remove': item + '@' + container,
                'move': item + '@' + room + '|' + room,
                'changeItem': change(item, item_attr),
                'changeRoom': change(room, room_attr),
                'changeInv': change(bag, bag_attr),
                'addProperty': 
             }

        index = code.find('!')
        command = code[:index]
        parameters = code[index+1:]

        return command, pt[command].parseString(parameters)[::2]

    def Action_Parse(self, action, code):
        """ Parses arity and item IDs from a user action command. """
        ''' Replaces the Action implementation of the same code in the interests
            of putting all the parsers under one umbrella.
            Also allows the possibility of verifying the existence of these 
            items. The action system has always been kind of a pain. '''
        pass
