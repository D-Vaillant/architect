"""
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
    
Action:
        Contains information about player actions. 

Inventory:
        Container class for the PC's inventory. Contains items which 
    can be used from the inventory menu.

File_Processor:
        Only used when initializing the Game; reads a text file
    and translates it into two different dictionaries: a Room info dict
    and a Thing info dict. These info dicts are used by the Room and
    Thing classes and encode all the information about the game.
"""

from rooms import Room
from actions import Action
from object_source import Inventory, Thing
from file_management import File_Processor
import re

V = False

class Game():
    cardinals = {'w':0, 's':1, 'n':2, 'e':3}
    special_actions = ['take']
    mcode_keywords = '[&!\-\+@#]'
    ERROR = {
        "exe_pass": "Invalid command.",
        "act_item_not_found": "It's not clear what thing " + 
                              "you're talking about.",
        "act_not_for_item": "That item cannot be used that way.",
        "act_using_rooms": "You can't do that with an entire room.",
        "act_already_holding": "You've already got one of those.",
        "act_taking_prop": "It doesn't seem like you could carry that.",
        "room_no_room_found": "WARNING: Incorrect room in mcode."
        }
    ACT_MSGS = {
        "Input < 2":"What do you want to do that to?",
        "0 < Max:":"You need to do that with something.",
        "Input > 0":"That doesn't make sense."
        }
    GAME_MSGS = {
        "beginning": "Welcome to the demo!",
        "quit": "Game closing."
        }
        
    #alias = {'_':loc, '^': }
    
    def __init__(self, rdata, tdata, adata, mdata):
        self.rooms = rdata
        self.things = tdata
        self.actions = adata
        """
        try: self.loc = self.mdata["firstRoom"]
        except KeyError: raise KeyError("Initial room either unspecified "+
                                        "or missing.")
        self.inventory = Inventory(ownedObjs) if mdata["ownedObjs"] \
                                              else Inventory()
        """
        self.loc = self.rooms["initial"]
        self.inventory = Inventory()
        self.setting_output = ''
        self.action_output = ''


    def prompt_exe(self, prompt):
        ''' Takes player input and passes the corresponding command to the
            corresponding player command function. '''
        i = prompt.lower().split() if prompt != '' else ''
        if i == []: i = ''

        if len(i) < 1: return
        if i[0] in self.cardinals.keys():
            self._move(i)
        elif i[0] in ['west', 'south', 'north', 'east']:
            self._move(i[0][0])
        elif i[0] in self.actions or self.special_actions:
            self.act(i)
        elif i[0] in ["inv", "i"]:
            self._inv("open")
        elif i[0] == '?':
            self._help(i[1:])
        elif i[0] == 'quit' or i[0] == 'q':
            self._puts(self.GAME_MSGS["quit"])
        else:
            self._puts(self.ERROR["exe_pass"])
        return        
            
    def _help(self, object):
        if object:
            pass
        else:
            self._puts("Movement: north, south, east, west")
            self._puts("Actions: " + ', '.join(self.actions))
        return
            
    ''' Classes of player commands: Moving, acting, and menu. '''
    # Move: Self-explanatory, right? Uses number to set current location to
    #       the room "in that direction" (specified via Room.links).
    def _move(self, direction):
        translated_direction = self.cardinals[direction[0][0]]
        try:
            self.loc = self.rooms[self.loc.links[translated_direction]]
        except KeyError:
            self._puts('I can\'t go that way.')
            return
        #self._room_update()
            
    # Act: Takes a command.
    """
    def act(self, command):
        ''' Action function. '''
        tmp = ' '.join(command[1:])

        # If no object specified.
        if tmp == '':
            if command[0] == "examine":
                self._puts(self.loc.on_examine())
                #self._puts(Thing.thing_printer([self.things[x] for x in self.loc.holding]))
            else: 
                self._puts(self.ERROR["act_item_not_found"])
        # Examining.
        elif command[0] == "examine":
            if tmp == "room":
                self._puts(self.loc.on_examine())
                #self._puts(Thing.thing_printer([self.things[x] for x in self.loc.holding]))
            elif tmp in self.loc.holding or tmp in self.inventory.holding:
                self._puts(self.things[tmp].examine_desc)
            else: self._puts(self.ERROR["act_item_not_found"])
        # Taking.
        elif command[0] == "take":
            if tmp == "room":
                self._puts(self.ERROR["act_using_rooms"])
            elif tmp in self.loc.holding:
                if self._alias(tmp).isProp:
                    self._puts(self.ERROR["act_taking_prop"])
                else:
                    self.inventory.add_item(tmp)
                    self.loc.holding.remove(tmp)
                    self._puts("Picked up the " + tmp + ".")
            elif tmp in self.inventory.holding:
                self._puts(self.ERROR["act_already_holding"])
            else:
                self._puts(self.ERROR["act_item_not_found"])
        # Other actions.
        else:
            if tmp == "room":
                self._puts(self.ERROR["act_using_rooms"])
            elif tmp in self.loc.holding or tmp in self.inventory.holding:
                try:
                    for x in self.things[tmp].action_dict[command[0]]:
                        self.mcode_main(x)
                except KeyError:
                    self._puts(self.ERROR["act_not_for_item"])
            else:
                self._puts(self.ERROR["act_item_not_found"])
        return
    """
    def act(self, command):
        """ Does actiony stuff. Don't ask me! """
        tmp = ' '.join(command[1:])
        
        if command[0] in self.special_actions:
            if command[0] == "take":
                if tmp == "room":
                    self._puts(self.ERROR["act_using_rooms"])
                elif tmp in self.loc.holding:
                    #tmp = self._alias(tmp)
                    if self._alias(tmp).isProp:
                        self._puts(self.ERROR["act_taking_prop"])
                    else:
                        self.inventory.add_item(tmp)
                        self.loc.holding.remove(tmp)
                        self._puts("Picked up the " + tmp + ".")
                #elif tmp in self.inventory.holding:
                #    self._puts(self.ERROR["act_already_holding"])
                else:
                    self._puts(self.ERROR["act_item_not_found"])
        else:
            ACT = self.actions[command[0]]
            command = command[1:]
            
            command = ACT.parse_string(command)
            
            if command[:2] == "#F:":
                self._puts(ACT_MSGS[command[2:]])
                
            try:
                for i, x in enumerate(command):
                    if x:
                        command[i] = self.things[x]
                tmp = ACT.call_action(command)
                for x in tmp: self.mcode_main(x)
            
            except KeyError:
                self._puts(self.ERROR["act_item_not_found"])
           
                
        return
        
    
    def _inv(self, command):
        """ Inventory menu commands. """
        if command == "open":
            self._puts(self.inventory.__str__())
        else: pass
        return

    
    # Functions for machine code. Includes main mcode function and ift,
    #    inv, obj, rom, and sys auxiliary functions as well as from tertiary 
    #    functions implemented by the auxiliary functions. '''

    def mcode_main(self, words):
        """ Main function for machine code.
        
        Takes a string of machine code and splits it up into a 
        pre-functional character, functional character, and a
        post-functional character. """
        if words == "pass": return
        print("INPUT: "+ str(words))
        type_code = words[:3]
        
        finder = re.search(Game.mcode_keywords, words)
        if finder is None:
            self._puts("MCode lacking functional character: " + words)
            raise AttributeError("No functional character found.")
        
        functional_char = words[finder.span()[0]]
        target = words[4:finder.span()[0]]
        parameters = words[finder.span()[1]:]
        #if type_code == 'prp': type_code = 'obj'
        getattr(self, type_code+"_func")(functional_char, target, parameters)
        #self._puts(type_code, functional_char, parameters)
        return
    
    def _alias(self, target):
        """ Turns a name into its appropriate room or thing. """
        
        if target == '_':
            return self.loc
        elif target == '$':
            return self.inventory
        elif target in self.rooms:
            return self.rooms[target]
        elif target in self.things:
            return self.things[target]
        else:
            raise NameError(target + " not a Thing, Room, or alias.")
        
    def ift_func(self, functional_char, thing_in_question,
                 condition):
        """ Conditional mcode processor.
        
        Isolates the condition from the post-functional part and enters an 
        if-ifelse-else structure to find which condition corresponds to
        the mcode. 
        
        If condition is true, runs each mcode line found after the >
        (separated by }) by calling mcode_main. Otherwise, runs mcode
        found after the <. """
                 
        # < divides the "on true" command from the "on false" one.
        condition = condition.split('<')
        else_condition = condition[1].split('}')
        condition = condition[0].split('}')
        
        # At this point condition has the following form:
        #          [parameter>mcode0, mcode1, mcode2,...]
        # We split up the parameter and the mcode0 part using the >,
        # assign parameter to second_thing, and assign mcode0 to condition[0].
        then_finder = re.search('>', condition[0])
        try:
            second_thing = condition[0][:then_finder.span()[0]]
            condition[0] = condition[0][then_finder.span()[1]:]
        except AttributeError:
            raise AttributeError("> not found.")
        
        # Turns second_thing into a class instance.
        second_thing = self._alias(second_thing)        
            
        # @: True if thing_in_question is in second_thing, where second_thing
        #    must be a room or an inventory (with a "holding" attribute).
        if functional_char == '@':
            try:
                if thing_in_question in second_thing.holding:
                    status = True
                else: 
                    status = False
            except KeyError:
                raise AttributeError("@ error.\n"+ second_thing.name + 
                                     " has no holding attribute.")

        # = : True if thing_in_question is identical with second_thing.
        #     Generally used in conjunction with the _ alias.
        elif functional_char == '=':
            if thing_in_question == second_thing:
                status = True
            else:
                status = False
                
        tmp = condition if status else else_condition
        for i in tmp: self.mcode_main(i)
        
        return
    
    def sys_func(self, functional_char, target, instruct):
        """ System mcode processor. Used to print messages to the terminal. """
        if V: self._puts("### Entering system functions.")
        if functional_char == '!':
            self._puts(instruct)
        else:
            pass
        return
    
    def inv_func(self, functional_char, target, instruct):
        """ Inventory mcode processor. Used for storage operations. """
        if V: self._puts("### Entering inventory functions.")
        
        if functional_char == '+':
            self.inventory.add_item(target)
        elif functional_char == '-':
            self.inventory.remove_item(target)
        else:
            pass
        return
        
    def rom_func(self, functional_char, target, instruct):
        """ Room mcode processor. Used to manipulate Rooms. """
        if V: self._puts("### Entering room functions.")

        #tmp_instruct = ' '.join(instruct)
        tmp_instruct = instruct
        
        # Changes a room name or _ into a Room class instance.
        target = self._alias(target)
        
        if functional_char == '+':
            target.holding.append(tmp_instruct)
        elif functional_char == '-':
            target.holding.remove(tmp_instruct)
        elif functional_char == '&':
            self._link(target, instruct[0], instruct[1:])
        elif functional_char == '#':
            try:
                attr = Room.codes['#' + instruct[:2]]
            except KeyError:
                raise AttributeError("No corresponding Room attribute.")
            self.change_var(target, attr, instruct[2:])
        return

    def obj_func(self, functional_char, target, instruct):
        """ Thing mcode processor. Used to manipulate Things. """
        if V: self._puts("### Entering object functions.")
        
        target = self._alias(target)
        
        if functional_char == '#':
            try:
                attr = Thing.codes['#'+instruct[:2]]
            except KeyError:
                raise AttributeError("No corresponding Thing attribute.")
            #self.change_var(target, attr, instruct[2:])
            if V: self._puts("#### Setting the new attribute now.")
            setattr(getattr(self, "things")[target.alias], attr, instruct[2:])
        return
    
    def change_var(self, target, attribute, new_desc):
        """ Tertiary function used to change the attributes of instances of
            Room and Thing. """
        try:
            setattr(target, attribute, new_desc) 
        except AttributeError:
            raise AttributeError(target + " does not have attribute "
                                        + attribute)
        return        
    
    def _link(self, source, direction, dest, isEuclidean = True):
        """ Tertiary function; establishes links between rooms.
                source ----direction----> dest
            If isEuclidean:
                dest ----opposite_dir----> source
            where opposite_dir should be clear. (N <-> S, W <-> E) """
            
        direction = self.cardinals[direction.lower()]
        dest = self._alias(dest)
        
        if isEuclidean:
            if source == dest:
                raise Error("Euclidean rooms enabled; no loops allowed.")
        source.links[direction] = dest.name
        if isEuclidean:
            if direction == 0: direction = 3
            elif direction == 1: direction = 2
            elif direction == 2: direction = 1
            elif direction == 3: direction = 0
            dest.links[direction] = source.name
        return

    '''
    def _on_entry(self):
        self._puts(self.loc.on_entry(), True)
        self._puts(
                Thing.thing_printer( \
                    [self.things[x] for x in self.loc.holding]),True)
        return
    '''

    def _room_update(self):
        thing_info = Thing.thing_printer([self.things[x] 
                                         for x in self.loc.holding])
        setting_info = self.loc.on_entry() + '\n'
        if thing_info:
            setting_info += thing_info + '\n'
        self._puts(setting_info, True)
        return

    ''' Main function. Takes user input, passes it to prompt_exe. '''
    def main(self):
        self._puts(self.GAME_MSGS['beginning'])
        self._room_update()
        '''
        prompt = ' '
        while (prompt[0] != 'q' and prompt[0] != 'quit'):
            x = input('> ')
            prompt = x.lower().split() if x != '' else ''
            if prompt == []: prompt = ' '
            self._prompt_exe(prompt)
        '''
        #raise NameError("Game finished.")
        return

    """ Functions which are involved in passing to GUI_Holder class. """
    def _puts(self, input_string, isSetting = False):
        if isSetting:
            self.setting_output = input_string
        else:
            self.action_output += input_string + '\n'

    def gets(self):
        self._room_update()
        returning = self.setting_output + '\n' + self.action_output
        self.action_output = ''
        return returning

with File_Processor('testgame_desc.txt') as F:
    room_info = F.room_info
    thing_info = F.thing_info
    action_info = F.action_info

def test_init():
    G = Game(Room.room_processor(room_info), \
             Thing.thing_processor(thing_info), \
             Action.action_processor(action_info), \
             None)
    return G

if __name__ == "__main__":
    G = test_init()
    G.main()
