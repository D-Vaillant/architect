''' 
game.py:
        The engine for the command-line based game. 
        Some vocabulary needs to be clarified, many things need to be
    implemented. I'll document the individual modules here.

MCode:
        A small programming language used to define how player actions
    involving Things can change Room attributes and other Things.

        I didn't want to define a new class for each room but different
    instances of classes can only differ semantically; changing Things
    required syntactic commands. Thus: I created a small system of commands
    which could be taken by an interpreter function which would then
    execute the commands.
        More information about the structure of MCode can be found in
    documentation/mcode_library.txt.

Room:
        Container class for the rooms that the PC enters.

        Also contains the room_reader function which takes a Room info dict
    (see File_Processor) to create a Room class dict, one of the input
    parameters for the Game class. 

Thing:
        Container class for the objects that the PC encounters. Come in two
    varieties, props and items. Props are static and cannot be moved
    once placed (generally in a room) while items can be placed and
    removed from an Inventory.

        Also contains the object_reader function which takes a Thing info dict
    and creates a Thing class dict, one of the input parameters for the
    Game class.

Inventory:
        Container class for the PC's inventory. Contains items which 
    can be used from the inventory menu.

File_Processor:
        Only used when initializing the Game; reads a text file
    and translates it into two different dictionaries: a Room info dict
    and a Thing info dict. These info dicts are used by the Room and
    Thing classes and encode all the information about the game.
'''

from rooms import Room
from object_source import Inventory, Thing
from file_management import File_Processor

class Game():
    cardinals = {'w':0, 's':1, 'n':2, 'e':3}
    actions = ['throw', 'examine', 'tap', 'unlock', 'take', 'leave', 'use']
    mcode_keywords = '[+-&@!*}{^]'
    #alias = {'_':loc, '^': }
    
    def __init__(self, rdata, tdata, firstRoom = 'initial', ownedObjs = {}):
        self.beginning = 'Welcome to the test!' 
        self.rooms = rdata
        self.things = tdata
        try: self.loc = self.rooms[firstRoom]
        except KeyError: raise KeyError("Initial room either unspecified "+
                                        "or missing.")
        self.inventory = Inventory({})
        
    ''' Classes of player commands: Moving, acting, and menu. '''
    # Move: Self-explanatory, right? Uses number to set current location to
    #       the room "in that direction" (specified via Room.links).
    def move(self, direction):
        try:
            translated_direction = self.cardinals[direction[0][0]]
            self.loc = self.rooms[self.loc.links[translated_direction]]
            self.loc.on_entry()
        except KeyError:
            print('I can\'t go that way.')
            
    # Act: Takes a command.
    def act(self, command):
        ''' Action commands. '''
        return  
    
    def inv(self, command):
        ''' Inventory menu commands. '''
        return
        
    def prompt_exe(self, i):
        ''' Takes player input and passes the corresponding command to the
            corresponding player command function. '''
        if len(i) < 1: return
        if i[0] in self.cardinals.keys():
            self.move(i)
        elif i[0] in ['west', 'south', 'north', 'east']:
            self.move(i[0][0])
        elif i[0] in self.actions:
            self.act(i)
        else:
            return
    
    # Functions for machine code. Includes main mcode function and ift,
    #    inv, obj, rom, and sys auxiliary functions as well as from tertiary 
    #    functions implemented by the auxiliary functions. '''

    def mcode_main(self, words):
        ''' Takes a string of machine code and splits it up into a 
            pre-functional character, functional character, and a
            post-functional character. '''
        type_code = words[:3]
        finder = re.search('[!]', words)
        if finder is None: raise TypeError("No functional character found.")
        
        functional_char = words[finder.span()[0]]
        target = words[4:words[finder.span()[0]]]
        parameters = words[finder.span()[1]:]
        #if type_code == 'prp': type_code = 'obj'
        getattr(self, type_code+"_func")(functional_char, target, parameters)
        #print(type_code, functional_char, parameters)
        return
    
    # ift_func: Conditional mcode processor. Isolates the condition from the
    # post-functional part and enters an if-ifelse-else structure to find which
    # condition corresponds to the mcode. If condition is true, runs each
    # mcode line found after the > (separated by }) by calling mcode_main.
    def ift_func(self, functional_char, thing_in_question, condition):
        condition = condition.split('}')
        
        # At this point condition has the following form:
        #          [parameter>mcode0, mcode1, mcode2,...]
        # We split up the parameter and the mcode0 part using the >,
        # assign parameter to second_thing, and assign mcode0 to condition[0].
        then_finder = re.search('>', condition[0])
        second_thing = condition[0][:then_finder.span()[0]]
        condition[0] = condition[0][then_finder.span()[1]:]
        
        # @: True if thing_in_question is in second_thing, where second_thing
        #    must be a room or an inventory (with a "holding" attribute).
        if functional_char == '@':
            try:
                if thing_in_question in second_thing.holding:
                    for x in condition: self.mcode_main(x)
            except AttributeError:
                raise AttributeError("@ error.\n"+
                      "Was checking if \""+thing_in_question.name+
                      "\" is in \""+second_thing.name+"\".")

        # = : True if thing_in_question is identical with second_thing.
        #     Generally used in conjunction with the _ alias.
        elif functional_char == '=':
            if thing_in_question == '_':
                thing_in_question = self.loc.name
            if thing_in_question == second_thing:
                for x in condition: self.mcode_main(x)

        return
    
    def sys_func(self, functional_char, target, instruct):
        """ System mcode processor. Used to print messages to the terminal. """
        print("Entering system functions.")
        if functional_char == '!':
            print(instruct)
        else:
            pass
        return
    
    def inv_func(self, functional_char, target, instruct):
        """ Inventory mcode processor. Used for storage operations. """
        print("Entering inventory functions.")
        if functional_char == '+':
            self.inventory.add_item(target)
        elif functional_char == '-':
            self.inventory.remove_item(target)
        else:
            pass
        return
        
    def rom_func(self, functional_char, instruct):
        """ Room mcode processor. Used to manipulate Rooms. """
        return

    def obj_func(self, functional_char, instruct):
        """ Thing mcode processor. Used to manipulate Things. """
        return
    
    def change_var(self, target, attribute, new_desc):
        ''' Tertiary function used to change the attributes of instances of
            Room and Thing. '''
        pointer = getattr(target, attribute) 
        new_desc = pointer
        return        
    
    def link(source, direction, dest, isEuclidean = True):
        ''' Tertiary function; establishes links between rooms.
                source ----direction----> dest
            If isEuclidean:
                dest ----opposite_dir----> source
            where opposite_dir should be clear. (N <-> S, W <-> E) '''
        if isEuclidean:
            if source == dest:
                raise Error("Euclidean rooms enabled; no loops allowed.")
        source[direction] = dest
        if direction == 0: direction = 3
        elif direction == 1: direction = 2
        elif direction == 2: direction = 1
        elif direction == 3: direction = 0
        target[direction] = source
        return


    ''' Main function. Takes user input, passes it to prompt_exe. '''
    def main(self):
        print(self.beginning)
        prompt = ' '
        while (prompt[0] != 'q' and prompt[0] != 'quit'):
            x = input('> ')
            prompt = x.lower().split() if x != '' else ''
            if prompt == []: prompt = ' '
            self.prompt_exe(prompt)
        #raise NameError("Game finished.")
        return "Game terminated."

with File_Processor('testgame_desc.txt') as F:
    room_info = F.room_info
    thing_info = F.thing_info

G = Game(Room.room_processor(room_info), Thing.thing_processor(thing_info))
#G.main()
