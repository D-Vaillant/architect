from pyparsing import oneOf, Optional, Literal, SkipTo, StringEnd, Or 

class Parser:
    def __init__(self, r, i, a):
        self.rooms = r
        self.items = i
        self.actions = a

        self.bp_commands = ['put', 'link', 'add', 'remove', 'move',
                            'change_room', 'change_item', 'change_inventory',
                           ]
        
    def BP_Parse(self, code):
        j = lambda x: ' '.join(x)
        item = oneOf(j(items.keys())) # string of all the item names
        item_attr = oneOf("name nick weight ground_desc examine_desc")
        room = oneOf(j(rooms.keys())) # string of all the room names
        dir = oneOf("W S N E")
        # string of all the names of different bags
        bag = oneOf(j(self.inventory.structured_holding.keys()))
        bag_attr = oneOf("add remove limit")
        container = '_' ^ room

        change = lambda x,y: x + '.' + y + '=' + SkipTo(StringEnd())

        # hash associating commands with their calling syntax
        # all syntax has the form ARG SYM ARG SYM ARG SYM..., to allow for
        # symbols to be easily ignored when passing parsed results
        pt = {
                'put' : SkipTo(StringEnd()),
                'link': room + '-' + dir + '->' + room,
                'add': item + '@' + container + Optional('.' + bag),
                'remove': item + '@' + container,
                'move': item + '@' + room + '|' + room,
                'change_item': change(item, item_attr)
                'change_room': change(room, room_attr)
                'change_inventory': change(bag, bag_attr),
             }

        index = code.find('!')
        command = code[:index]
        parameters = code[index+1:]

        return command, pt[command].parseString(parameters)[::2]
