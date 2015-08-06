"""
Project name: Architect

game.py:
        The engine for the command-line based game. 
        Some vocabulary needs to be clarified, many things need to be
    implemented. I'll document the individual modules here.

Blueprint:
        A domain specific language.
        
        I didn't want to define a new class for each room but different
    instances of classes can only differ semantically; changing Items
    required syntactic commands. Thus: I created a small system of commands
    which could be taken by an interpreter function which would then
    execute the commands.
        More information about the structure of Blueprint can be found in
    documentation/blueprint_library.txt.

Room:
        Container class for the rooms that the PC enters.

        Also contains the room_reader function which takes a Room info dict
    (see File_Processor) to create a Room class dict, one of the input
    parameters for the Game class. 

Item:
        Container class for the objects that the PC encounters. Come in two
    varieties, props and items. Props are static and cannot be moved
    once placed (generally in a room) while items can be placed and
    removed from an Inventory.

        Also contains the object_reader function which takes a Item info dict
    and creates a Item class dict, one of the input parameters for the
    Game class.
    
Action:
        Contains information about player actions. 

Inventory:
        Container class for the PC's inventory. Contains items which 
    can be used from the inventory menu.

InfoCollector:
        Only used when initializing the Game; reads a JSON file
    and translates it into three different dictionaries: a Room info dict,
    an Action info dict, and a Item info dict. These info dicts are used by
    their respective classes and encode all the information about the game.
"""

from rooms import Room
from actions import Action
from inventory import Inventory
from item import Item
from json_reader import InfoCollector
import re

# Verbose option.
V = False

class Game():
    cardinals = {'w':0, 's':1, 'n':2, 'e':3}
    special_actions = ['take'] ## Special actions are... weird.
    blueprint_keywords = '[&!\-\+@#]' ## Blueprint needs to be reworked.
    ERROR = {
        "exe_pass": "Invalid command.",
        "ambiguity": "Be more specific!",
        "item_not_found": "It's not clear what thing " 
                          "you're talking about.",
        "act_not_for_item": "That item cannot be used that way.",
        "act_using_rooms": "You can't do that with an entire room.",
        "act_already_holding": "You've already got one of those.",
        "act_taking_prop": "It doesn't seem like you could carry that.",
        "room_no_room_found": "WARNING: Incorrect room in Blueprint."
        }
    ACT_MSGS = {
        "Input < Min":"What do you want to do that to?",
        "0 < Min:":"You need to do that with something.",
        "Input > Min":"That doesn't make sense."
        }
    GAME_MSGS = {
        "beginning": "Welcome to the demo!",
        "quit": "Game closing."
        }
        
#---------------------------- Initialization ---------------------------------
    def __init__(self, rdata, tdata, adata, mdata):
        M = lambda x: x if x in mdata else None

        self.rooms = Room.room_processor(rdata)
        self.items = Item.item_processor(tdata)
        self.item_names = {t.name:t.id for t in self.items.values()}
        self.actions = Action.action_processor(adata)
        self.inventory = Inventory(M('inventory')) if M('inventory') \
                                                   else Inventory()
        
        self._populate()
        
        # For eventual implementation of meta-data entry.
        ## self._meta_processor(mdata)
        self.isCLI = M('isCLI') or False
        
        self.loc = self.rooms["initial"]
        self.setting_output = ''
        self.action_output = ''
        
    def _populate(self):
        for room in self.rooms.values():
            try:
                ##if V: print([t for t in room.holding])
                room.holding = [self._IDtoItem(_) for _ in room.holding]
            except KeyError:
                raise KeyError("Room holding non-existent item.")
        """     
        if self.inventory:
            for location, bag in self.inventory.structured_holding.items():
                self.inventory.structured_holding[location] = \
                    {self._IDtoItem(_) for _ in bag}        
        """
        return        
        
    def _meta_processor(self, raw_mdata):
        try: 
            firstRoomID = raw_mdata["firstRoom"]
            self.loc = self._alias(firstRoomID)
        except KeyError: 
            raise KeyError("Initial room unspecified.")
        except NameError:
            raise NameError("Initial room not found.")
        
#------------------------------ Utility Functions ----------------------------

    ##def _getItem(self, item_id, holder):
    ##    return self.items[item_id] if item_id in holder.holding else None
    #!! Deprecated, I'm pretty sure.
    
#----------------------------- Engine Methods --------------------------------
## Used in BP Code implementation. 

    def _bpRouter(self, args):
        getattr(self, '_'+args[0])(*args[1])

    def _add(self, item, container, target = "main"):
        print(item, container)

        item = self._IDtoItem(item)
        if container == '_':
            container = self.inventory
            container.add(item, target)
        else:
            container = self.rooms[container]
            container.add(item)

    def _remove(self, item, container, target = "main"):
        if container == '_':
            container = self.inventory
            container.remove(item, target)
        else:
            container = self._IDtoItem(container)
            container.remove(item)
            

    def _move(self, moved_item, source, target):
        """ Removes moved_item from source and adds it to target. """
        if moved_item in source:
            try: 
                target.add(moved_item)
                source.remove(moved_item)
            except AttributeError:
                raise AttributeError("Target lacks add() method.")
        else:
            raise AttributeError("Item not in source.")
        return

    def _addProperty(self, property, item):
        item.setProperty(property)

    def _removeProperty(self, property, item):
        item.setProperty(property, False)

    def _setItemDesc(self, type, text):
        if(item.setDescription(type, text)):
            raise AttributeError("{}_desc for {} failed.".format(type, 
                                                                 item.id))

    
    def _IDtoItem(self, id):
        """ Returns an Item instance W such that W.id = id. """
        try:
            return self.items[id]
        except KeyError:
            raise NameError("No item with ID {}.".format(id))
        
    #! Figure out how I'm going to handle this propertly.
    #  IDtoItem gets rid of the need for the ID grabbing.
    #  It makes sense to implement SymbolToContainer and SymbolToRoom
    #  methods in order to capture the other things I want to do.
    #        Depends on how Blueprint is implemented!
    def _alias(self, target):
        """ Turns an ID into its appropriate room or item. """
        
        if target == '_':
            return self.loc
        elif target == '$':
            return self.inventory
        elif target in self.rooms:
            return self.rooms[target]
        elif target in self.item_names:
            return self.items[self.item_names[target]]
        else:
            raise NameError(target + " not a Item, Room, or alias.")
            

#-------------------------------- User Methods -------------------------------

    def prompt_exe(self, prompt):
        """ Takes user input and passes it to the appropriate method. """
            
        # Turns string inputs into arrays of strings.
        i = prompt.lower().split() if prompt else ''
        
        # Does nothing if empty command is entered.
        if len(i) < 1: pass

        # Call _move if a movement command is entered.
        elif i[0] in self.cardinals.keys():
            self._movePlayer(i[0])
        elif i[0] in ['west', 'south', 'north', 'east']:
            self._movePlayer(i[0][0])

        # Inventory call.
        elif i[0] in ["inv", "i"]:
            self._inv("open")
            
        # Call _act if an action is entered.
        elif i[0] in self.actions or \
             i[0] in self.special_actions:
            if V: print("Treating ", i[0], " as an action.")
            self._act(i)
        
        # System calls. ? calls help.
        #!! Needs to be worked out.
        elif i[0] == '?':
            self._help(''.join(i[1:]))
            
        # Puts Quit message.
        elif i[0] == 'quit' or i[0] == 'q':
            self._puts(self.GAME_MSGS["quit"])
        
        # Puts an error message if an unrecognised command is entered.
        else:
            self._puts(self.ERROR["exe_pass"])
            
        if V: print()
        return        
            
    def _help(self, object):
        """ Puts help messages. """
        #!! Work needed here.
        if object:
            pass
        else:
            self._puts("Movement: north, south, east, west")
            self._puts("Actions: " + ', '.join(self.actions))
        return
            
# ----------------------- User/Designer Interface ----------------------------

    def _local(self):
        return self.loc.holding+self.inventory.holding  
        
    def _itemNametoID(self, item_name):
        search_arr = [x for x in self._local() if item_name in x.name]
        if len(search_arr) == 1:
            return search_arr[0].id
        elif len(search_arr):
            self._puts(self.ERROR["ambiguity"])
            return None
        else: 
            self._puts(self.ERROR["item_not_found"])
            return None
    
    def _movePlayer(self, direction):
        """ Attempts to change self.loc in response to movement commands. """
        # Transforms letters to Room.links array index (0-3).
        translated_direction = self.cardinals[direction[0][0]]
        
        try:
            self.loc = self.rooms[self.loc.links[translated_direction]]
        except KeyError:
            self._puts("I can't go that way.")
            return
        #self._room_update()
            
    # Act: Takes a command.
    # Deprecated by new action system.
    """
    def act(self, command):
        ''' Action function. '''
        tmp = ' '.join(command[1:])

        # If no object specified.
        if tmp == '':
            if command[0] == "examine":
                self._puts(self.loc.on_examine())
                #self._puts(Item.item_printer([self.items[x] 
                     for x in self.loc.holding]))
            else: 
                self._puts(self.ERROR["act_item_not_found"])
        # Examining.
        elif command[0] == "examine":
            if tmp == "room":
                self._puts(self.loc.on_examine())
                #self._puts(Item.item_printer([self.items[x] 
                     for x in self.loc.holding]))
            elif tmp in self.loc.holding or tmp in self.inventory.holding:
                self._puts(self.items[tmp].examine_desc)
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
                    for x in self.items[tmp].action_dict[command[0]]:
                        self.blueprint_main(x)
                except KeyError:
                    self._puts(self.ERROR["act_not_for_item"])
            else:
                self._puts(self.ERROR["act_item_not_found"])
        return
    """
    
    def _act(self, command):
        """ Does actiony stuff. Don't ask me! """
        if V: print("Running action prompt.")
       
        # Parses input as [action, specifics*].
        action = command[0]
        specifics = ' '.join(command[1:])
        
        # Hard coding of some actions like take, examine.
        ## Could theoretically be rolled into the Action class as well.
        if action in self.special_actions:
            if V: print("Special action being run.")
            self._special_act(action, specifics)
                    
        # User-specified actions.
        elif action in self.actions:
            if V: print("Ordinary action being run.")
            self._user_act(action, specifics)
            
        else:
            print("Non-action. Why are we here?")
        return
        
    def _special_act(self, action, specifics):
        if action == "take":
            try: 
                specifics = self._IDtoItem(self._itemNametoID(specifics))
            except NameError: 
                if V: print("Failed to get Item: {}".format(specifics)) 
            
            if specifics == "room": # More of an Easter Egg.
                if V: print("Taking: Room.")
                self._puts(self.ERROR["act_using_rooms"])
            elif specifics:
                if V: print("Taking: ", specifics)
                if specifics.isProp:
                    self._puts(self.ERROR["act_taking_prop"])
                else:
                    self.inventory.add_item(specifics)
                    self.loc.holding.remove(specifics)
                    self._puts("Picked up the " + specifics.name + ".")
            ## elif specifics in self.inventory.holding:
            ##     self._puts(self.ERROR["act_already_holding"])
            else:
                self._puts(self.ERROR["act_item_not_found"])
                    
    def _user_act(self, action, specifics):
        """ Text processing part. """
        breaker = True
        
        # Turns action names into Action instances.
        action = self.actions[action]
        
        # Transforms specifics into either an error message string
        # or an array of Item names.
        specifics = action.parseString(specifics)
        
        
        # If parseString returns a "$! " prefixed string, put
        # an error message.
        if specifics and specifics[:2] == "$! ":
            self._puts(ACT_MSGS[specifics[2:]])
        
        # Turns the parsed string into (hopefully) an array of Item IDs.
        try:
            specifics = specifics.split()
            print(specifics)
            for i, x in enumerate(specifics):
                if x:
                    print("Working! ", i, x)
                    try:
                        # Changes specifics into an array of Items.
                        x = self._itemNametoID(x)
                        specifics[i] = self._IDtoItem(x) 
                        print(specifics)
                    except KeyError: 
                        # If one of the item IDs doesn't correspond to the ID 
                        # of an Item, put a "Cannot be found." message.
                        self._puts(self.ERROR["act_item_not_found"])
                        breaker = False
                        
        except AttributeError:
            if specifics != 0: 
                raise AttributeError("specifics is not splittable.")

        """ Acting part. """
        if breaker:
            # Calls the action, returning an array of instructions and runs it.
            bp_code = action.call(specifics)
            for x in bp_code: self.blueprint_main(x)

    def _inv(self, command):
        """ Inventory menu commands. """
        if command == "open":
            self._puts(self.inventory.__str__())
        else: pass
        return

    
# ----------------------- Designer/Engine Interface --------------------------
    """ A great deal of work must be done here. Revamping this whole thing, 
        in all probability. """
    
    def blueprint_main(self, words):
        """ Main function for Blueprint code.
        
        Takes a string of BP code and splits it up into a 
        pre-functional character, functional character, and a
        post-functional character. """
        if words == "pass": return
        print("INPUT: "+ str(words))
        type_code = words[:3]
        
        finder = re.search(Game.blueprint_keywords, words)
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
        
    def ift_func(self, functional_char, thing_in_question,
                 condition):
        """ Conditional blueprint processor.
        
        Isolates the condition from the post-functional part and enters an 
        if-ifelse-else structure to find which condition corresponds to
        the Blueprint code. 
        
        If condition is true, runs each BP code line found after the >
        (separated by }) by calling blueprint_main. Otherwise, runs BP code
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
        

        ### Redo inventory isHolding checks.
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
        for i in tmp: self.blueprint_main(i)
        
        return
    
    def sys_func(self, functional_char, target, instruct):
        """ System mcode processor. Used to print messages to the terminal. """
        if V: self._puts("### Entering system functions.")
        if functional_char == '!':
            self._puts(instruct)
        else:
            pass
        return
    
    ### Inventory complication project continues onwards.
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
    

    ### Do some cleaning up here.
    def rom_func(self, functional_char, target, instruct):
        """ Room mcode processor. Used to manipulate Rooms. """
        if V: self._puts("### Entering room functions.")

        #tmp_instruct = ' '.join(instruct)
        tmp_instruct = instruct
        
        # Changes a room name or _ into a Room class instance.
        target = self._alias(target)
        
        ### Aren't they suppose.d to hold instances, not names?
        if functional_char == '+':
            target.holding.append(tmp_instruct)
        elif functional_char == '-':
            target.holding.remove(tmp_instruct)
            
        elif functional_char == '&':
            self._link(target, instruct[0], instruct[1:])
            
        ### Make sure this works properly.
        elif functional_char == '#':
            try:
                attr = Room.codes['#' + instruct[:2]]
            except KeyError:
                raise AttributeError("No corresponding Room attribute.")
            self.change_var(target, attr, instruct[2:])
        return

    def obj_func(self, functional_char, target, instruct):
        """ Item mcode processor. Used to manipulate Items. """
        if V: self._puts("### Entering object functions.")
        
        target = self._alias(target)
        
        ### Give this a looksee.
        if functional_char == '#':
            try:
                attr = Item.codes['#'+instruct[:2]]
            except KeyError:
                raise AttributeError("No corresponding Item attribute.")
            #self.change_var(target, attr, instruct[2:])
            if V: self._puts("#### Setting the new attribute now.")
            setattr(getattr(self, "things")[target.alias], attr, instruct[2:])
        return
    
    ### Is this even used?
    def change_var(self, target, attribute, new_desc):
        """ Tertiary function used to change the attributes of instances of
            Room and Item. """
        try:
            setattr(target, attribute, new_desc) 
        except AttributeError:
            raise AttributeError(target + " does not have attribute "
                                        + attribute)
        return        
    
    ## Should probably be a Room staticmethod.
    def _link(self, source, direction, dest, isEuclidean = True):
        """ Establishes links between rooms.
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
                Item.thing_printer( \
                    [self.things[x] for x in self.loc.holding]),True)
        return
    '''

# --------------------------- GUI/User Interface -----------------------------
    
    def _room_update(self):
        item_info = Item.item_printer(self.loc.holding)
        setting_info = self.loc.onEntry() + '\n'
        if item_info:
            setting_info += item_info + '\n'
        self._puts(setting_info, True)
        return

    ''' Main function. Takes user input, passes it to prompt_exe. '''
    def main(self):
        """ """
        self._puts(self.GAME_MSGS['beginning'])
        self._room_update()
        #raise NameError("Game finished.")
        return
        
    def cliMain(self):
        self.main()
        prompt = ' '
        while (prompt[0] != 'q' and prompt[0] != 'quit'):
            print(self.gets())
            prompt = input('> ').lower()
            ##prompt = x.split() if x != '' else ''
            if prompt == '': prompt = ' '
            self.prompt_exe(prompt)        

    """ Functions which are involved in passing to GUI_Holder class. """
    
    def _puts(self, input_string, is_setting = False):
        """ Adds text to the output buffer. """
        if is_setting:
            self.setting_output = input_string
        else:
            self.action_output += input_string + '\n'

    def gets(self):
        """ Returns text from the output buffer and clears it. """
        self._room_update()
        returning = self.setting_output + '\n' + self.action_output
        self.action_output = ''
        return returning


# ------------------------- Testing -----------------------------------------

def gui_init():
    F = InfoCollector()
    F.meta_info['isCLI'] = False
    G = Game(*F.output())
    return G

if __name__ == "__main__":
    G = test_init()
    G.cliMain()
