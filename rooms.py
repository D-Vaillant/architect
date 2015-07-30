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
        self.entry_desc = self.initializeEntryDesc(d('desc'))
        self.holding = d('hold') or ''
        ##if d('data'): self.data = []

        self.is_visited = False

    def initializeEntryDesc(self, json_entry):
        if type(json_entry) != "dict":
            return {0:json_entry}
        else:
            return {index:entry for index, (key, entry)
                                in enumerate(sorted(json_entry.items()))}
            
    
    def onEntry(self):
        """ Runs whenever a room is entered. """
        self.is_visited = True
        out = "\n".join([self.entry_desc[_]
                        for _ in sorted(self.entry_desc)])
        return out
        
    def link(self, linked_room, dir):
        self.links[dir] = linked_room

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

        """
        if room_link_dict: 
            for x in room_link_dict:
                try:
                    r[x].link_processor(room_link_dict[x])
                except KeyError:
                    print("Tried to set links of a room which doesn't exist.")
                    print("Relevant line: ", x)
        """

   
