""" rooms.py:
        Implementation of Rooms for Game.
"""
__author__ = "David Vaillant"

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
