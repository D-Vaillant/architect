""" rooms.py:
        Implementation of Rooms for Game.
"""
__author__ = "David Vaillant"

class Room():
    ''' Room class. '''
    codes = {
        '#NA':'name',
        '#EN':'entry_desc',
        '#RE':'reentry_desc',
        '#EX':'examine_desc',
        '#IL':'item_location',
            }
            
    def d(self, room_dict, i):
        """ Used in __init__ as error exception. """
        try:
            return room_dict[i]
        except:
            return 'N/A'
        
    def __init__(self, r):
        self.links = [x for x in r['L']]
        self.name = self.d(r, 'NA')
        self.entry_desc = self.d(r, 'EN')
        self.examine_desc = self.d(r, 'EX')
        self.reentry_desc = self.d(r, 'RE')
        self.holding = [x for x in self.d(r, 'IL').split(' | ')] if (
                              self.d(r, 'IL') != '') else ['']
        self.is_visited = False
                              
    def on_entry(self):
        ''' Runs whenever a room is entered. '''
        if self.is_visited:
            print(self.reentry_desc)
        else:
            print(self.entry_desc)
            self.is_visited = True
        print(self.print_holding())
        return
        
    def on_examine(self):
        if self.examine_desc == "N/A":
            print("There's not much to see here.")
        else: 
            print(self.examine_desc)
        print(self.print_holding())
        return
        
    def print_holding(self):
        """ Returns a string describing all the Things in the Room """
        out_str = ''
        for x in self.holding:
            if x.ground_desc == 'pass':
                str = str + "\nThere is a " + x.alias + " here."
            else:
                str = str + "\n" + x.ground_desc
            return str
            
    def room_processor(room_info_dict, room_link_dict = None):
        """ Takes a Room info dictionary and creates a Room class dictionary.

        If a link info dictionary is provided, runs each Room's
        link_processor method to set the attribute. """
        r = {}
        # Iterates through the dictionary's keys and creates a new Room using
        # the associated value (a Room info dictionary).
        for x in room_info_dict.keys():
            r[x] = Room(room_info_dict[x])
        if room_link_dict: 
            for x in room_link_dict:
                try:
                    r[x].link_processor(room_link_dict[x])
                except KeyError:
                    print("Tried to set links of a room which doesn't exist.")
        return r
    
    def __str__(self):  
        string = "Name: " + self.name + ".\n"
        string = string + "First entry message: " + self.entry_desc + "\n"
        string = string + "Reentry message: " + self.reentry_desc + "\n"
        string = string + "On examine: " + self.examine_desc + "\n"
        string = string + "Items contained: " + self.holding + "\n"
    
        return string  
