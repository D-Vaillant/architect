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

JSON_Reader:
        Only used when initializing the Game; reads a JSON file
    and translates it into three different dictionaries: a Room info dict,
    an Action info dict, and a Item info dict. These info dicts are used by
    their respective classes and encode all the information about the game.
"""

from ontology import Room, Action, Inventory, Item
from utils import Parser, JSON_Reader

import re

# Verbose option.
V = True

class Game():
    cardinals = {'w':0, 's':1, 'n':2, 'e':3}
    special_actions = ['take'] ## Special actions are... weird.
    ##TODO: Figure out the role of special actions.

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
        "0 < Min":"You need to do that with something.",
        "Input > Max":"That doesn't make sense."
        }
    GAME_MSGS = {
        "beginning": "Welcome to the demo!",
        "quit": "Game closing."
        }

    special_actions = {
        "take": Action({
            "id": "take",
            "0" : "puts!What are you picking up?",
            "1" : OrderedDict(
                {"p:prop":  "puts!That's too big to carry.",
                 ""      :  "move!%i"})
            })
                     }

#---------------------------- Initialization ---------------------------------

    def __init__(self, rdata, tdata, adata, mdata):
        M = lambda x: x if x in mdata else None

        self.rooms = Room.room_processor(rdata)
        self.items = Item.item_processor(tdata)
        ##self.item_names = {t.name:t.id for t in self.items.values()}
        self.actions = Action.action_processor(adata)


        self.inventory = Inventory(M('inventory')) if M('inventory') \
                                                   else Inventory()

        self.parser = Parser(self.rooms, self.items,
                             self.actions, self.inventory)

        self._populate()

        # For eventual implementation of meta-data entry.
        ## self._meta_processor(mdata)
        self.isCLI = M('isCLI') or False

        self.loc = self.rooms["initial"]
        self.setting_output = ''
        self.action_output = ''

        # --- Overarching Settings ---
        # Euclidean forces links to be irreflexive and symmetric.
        self.is_euclidean = M('isEuclidean') or True

    def _populate(self):
        for room in self.rooms.values():
            R = lambda i: self._IDtoRoom(i) if i else None
            try:
                room.links = [R(x) for x in room.links]
            except KeyError:
                raise KeyError("Room {} has invalid links: {}".format(
                                                     room,room.links))
            try:
                ##if V: print([t for t in room.holding])
                room.holding = [self._IDtoItem(_) for _ in room.holding]
            except KeyError:
                raise KeyError("Room {} holding non-existent items: {}.".format(
                                                             room,room.holding))
            # TODO: Figure out why Inventory is already holding Items.
            """
        if self.inventory:
            for location, bag in self.inventory.holding.items():
                tmp_bag = {self._IDtoItem(_) for _ in bag}
                self.inventory.holding[location] = tmp_bag
            """
        return

    # TODO: Integrate this into init; it's too sad on its own.
    #def _meta_processor(self, raw_mdata):
    #    try:
    #        firstRoomID = raw_mdata["firstRoom"]
    #        self.loc = self._alias(firstRoomID)
    #    except KeyError:
    #        raise KeyError("Initial room unspecified.")
    #    except NameError:
    #        raise NameError("Initial room not found.")

# --------------------------- GUI-User Interface -----------------------------

    def main(self):
        """ Takes user input, passes it to prompt_exe. """
        self._puts(self.GAME_MSGS['beginning'])
        self._room_update()
        #raise NameError("Game finished.")
        return

    def cliMain(self):
        """ Takes user input via the CLI, passes it to prompt_exe. """
        self.main()
        prompt = ' '
        while (prompt[0] != 'q' and prompt[0] != 'quit'):
            print(self.gets())
            prompt = input('> ').lower()
            ##prompt = x.split() if x != '' else ''
            if prompt == '': prompt = ' '
            self.prompt_exe(prompt)

    def _room_update(self):
        """ Adds item and setting information to the output buffer. """
        item_info = Item.item_printer(self.loc.holding)
        setting_info = self.loc.onEntry() + '\n'
        if item_info:
            setting_info += item_info + '\n'
        self._puts(setting_info, True)
        return

    """ Functions involved in passing to GUI_Holder class. """

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

# ------------------------------- User Methods ---------------------------------

    def prompt_exe(self, prompt):
        """ Takes user input and passes it to the appropriate method. """
        # Turns string inputs into array of strings.
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

        return

    def _help(self, object):
        """ Puts help messages. """
        #!! Work needed here.
        if object:
            pass
        else:
            self._puts("Movement: north, south, east, west")
            self._puts("Actions: " + ', '.join(
                                          [a for a,A in self.actions.items() 
                                                     if A.isKnown]))
        return

# ---------------------------- Utility Functions -------------------------------

    def _local(self):
        """ Returns a list of Items near the player. """
        return self.loc.holding+self.inventory.holding_list

    def _IDtoRoom(self, id):
        """ Returns a Room instance R such that R.id = id. """
        try:
            return self.rooms[id]
        except KeyError:
            raise KeyError("No room with ID {}.".format(id))

    def _scopeGetter(self, scope):
        """ Takes a scope and returns a corresponding list of Items.

            scope parameters:
                held:       in inventory
                held.bag:   in inventory.holding[bag]
                around:     in self.loc
                local:      in self.loc or inventory
                [room_ids]: in one of the given rooms
                global:     in anything
        """
        val_list = []
        if scope == "held":
            val_list = self.inventory.holding_list
        elif "held." in scope:
            val_list = self.inventory.holding[scope[5:]]
        elif scope == "around":
            val_list = self.loc.holding
        elif scope == "local":
            val_list = self.loc.holding+self.inventory.holding_list
        elif scope == "global":
            val_list = list(self.items.values)
        return val_list

    def _IDtoItem(self, id, scope="global"):
        """ Returns an Item instance W such that W.id = id. """
        try:
            return self.items[id]
        except KeyError:
            raise NameError("No item with ID {}.".format(id))

    def _itemNametoItem(self, item_name, scope="local"):
        """ Gets an Item from its name or nickname.
                By default, only looks for Items in the local scope.
        """
        search_arr = [x for x in self._scopeGetter(scope)
                              if (item_name == x.name
                              or item_name == x.nickname)]
        if len(search_arr) == 1:
            return search_arr[0]
        ## TODO: Revamp this so that the error reporting isn't handled by this.
        ## Probably best to use error numbers.
        elif len(search_arr):
            self._puts(self.ERROR["ambiguity"])
            return 99 # Error code for ambiguity.
        else:
            self._puts(self.ERROR["item_not_found"])
            return -1

    #def _itemNametoItem(self, item_name, **kwargs):
    #    """ Composition of _itemNametoID and _IDtoItem. """
    #    _ = self._itemNametoID(item_name, **kwargs)
    #    return self._IDtoItem(_) if (type(_) is not int) else None

# ------------------------- User-Engine Interface ------------------------------
# Includes some simple Engine methods (_movePlayer, let's be real here) and
# the first component of the Action pipeline.

    def _movePlayer(self, direction):
        """ Attempts to change self.loc in response to movement commands. """
        # Transforms letters to Room.links array index (0-3).
        translated_direction = self.cardinals[direction[0][0]]
        destination = self.loc.links[translated_direction]

        if destination is not None: 
            self.loc = destination 
        else: 
            self._puts("I can't go that way.")

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
        # TODO: Write an actual docstring.
        """ Does actiony stuff. Don't ask me! """
        if V: print("Running action prompt.")

        # Parses input as [action, specifics*].
        action = command[0]
        specifics = ' '.join(command[1:])

        # Hard coding of some actions like take, examine.
        ## Could theoretically be rolled into the Action class as well.
        if action in self.special_actions:
            if V: print("Special action being run.")
            self._specialAct(action, specifics)

        # User-specified actions.
        elif action in self.actions:
            if V: print("Ordinary action being run.")
            self._userAct(action, specifics)

        else:
            print("Non-action. Why are we here?")
        return

    def _specialAct(self, action, specifics):
        # TODO: Docstring.
        if action == "take":
            try:
                specifics = self._itemNametoItem(specifics)
            ## elif specifics in self.inventory.holding:
            ##     self._puts(self.ERROR["act_already_holding"])
            except NameError:
                self._puts(self.ERROR["act_item_not_found"])
            else:
                if V: print("Taking: ", specifics)
                if specifics.isProp:
                    self._puts(self.ERROR["act_taking_prop"])
                else:
                    self.inventory.add(specifics)
                    self.loc.holding.remove(specifics)
                    self._puts("Picked up the " + specifics.name + ".")

    def _userAct(self, action, specifics):
        # TODO: Docstring.
        """ Text processing part. """
        # Turns action names into Action instances.
        action = self.actions[action]

        # Transforms specifics into either an error message string
        # or an array of Item names.
        # See Parser.actionParse.__doc__.
        specifics = self.parser.actionParse(action, specifics)
        # If parseString returns a "$! " prefixed string, put
        # an error message.
        if specifics and specifics[:3] == "$! ":
            self._puts(self.ACT_MSGS[specifics[3:]])
        # Turns the parsed string into (hopefully) an array of Item IDs.
        else:
            if V: print(specifics)

            try:
                # Setting specifics to a list of Item instances.
                specifics = [self._itemNametoItem(_) for _ in specifics] \
                                                     if specifics else 0
                if V:
                    print("Specifics generated:")
                    try:
                        for _ in specifics:
                            print("{}".format(_.id))
                    except AttributeError:
                        print("{} is not an Item!".format(_))
                    except TypeError:
                        print("{} is 0!".format(specifics))

            except KeyError:
                self._puts(self.ERROR["act_item_not_found"])
            else:
                bp_code = action.call(specifics)
                if V: print("Generated BP Code: {}".format(bp_code))
                for x in bp_code: self._bpRouter(self.parser.bpParse(x))

    def _inv(self, command):
        """ Inventory menu commands. """
        if command == "open":
            self._puts(self.inventory.__str__())
        else: pass
        return

# ------------------------------ Engine Methods --------------------------------
# Used in BP Code implementation.

    def _bpRouter(self, args):
        if args == "pass": return
        else: getattr(self, '_'+args[0])(*args[1])

    def _add(self, item, container, target = "main"):
        """ Adds an Item to a container. """
        item = self._IDtoItem(item)
        if container == '_':
            container = self.inventory
            container.add(item, target)
        else:
            container = self._IDtoRoom(container)
            container.add(item)

    def _remove(self, item, container, target = None):
        """ Removes an Item from a container. """
        item = self._IDtoItem(item)
        if container == '_':
            container = self.inventory
            container.remove(item, target)
        else:
            container = self._IDtoRoom(container)
            container.remove(item)

    def _link(self, source, dir, dest):
        dir = self.cardinals[dir.lower()]
        source = self._IDtoRoom(source)
        dest = self._IDtoRoom(dest)

        source.link(dest, dir, self.is_euclidean)

    def _move(self, moved_item, source, target):
        """ Removes moved_item from source and adds it to target. """
        if moved_item in source:
            try:
                target.add(moved_item)
            except AttributeError:
                raise AttributeError("Target lacks add() method.")
            try:
                source.remove(moved_item)
            except AttributeError:
                raise AttributeError("Source lacks remove() method.")
        else:
            raise AttributeError("Item not in source.")
        return

    def _addProperty(self, item, property):
        item = self._IDtoItem(item)
        item.setProperty(property)

    def _removeProperty(self, item, property):
        item = self._IDtoItem(item)
        item.setProperty(property, False)

    def _changeItem(self, item, attr, text):
        item = self._IDtoItem(item)
        if '_desc' in attr:
            print("WARNING: You should be calling changeDescription.")
            return
        try:
            setattr(item, attr, text)
        except AttributeError:
            raise AttributeError("%s is not an item attribute."%attr)

    def _changeDescription(self, object, type, index=0, text=''):
        pass

    def _changeRoom(self, room, attr, text):
        room = self._IDtoRoom(room)
        try:
            setattr(room, attr, text)
        except AttributeError:
            raise AttributeError("%s is not a room attribute."%attr)

    def _changeInv(self, bag, attr, text):
        inv = self.inventory()
        bag = inv.structuredHolding[bag]
        # TODO: Implement "add bag", "remove bag", and "change bag limits".
        return

############ Graveyard of Blueprint Past ###################################
#
#   Implemented aspects are wiped clean here.
#
#    def ift_func(self, functional_char, thing_in_question,
#                 condition):
#        """ Conditional blueprint processor.
#
#        Isolates the condition from the post-functional part and enters an
#        if-ifelse-else structure to find which condition corresponds to
#        the Blueprint code.
#
#        If condition is true, runs each BP code line found after the >
#        (separated by }) by calling blueprint_main. Otherwise, runs BP code
#        found after the <. """
#
#        # < divides the "on true" command from the "on false" one.
#        condition = condition.split('<')
#        else_condition = condition[1].split('}')
#        condition = condition[0].split('}')
#
#        # At this point condition has the following form:
#        #          [parameter>mcode0, mcode1, mcode2,...]
#        # We split up the parameter and the mcode0 part using the >,
#        # assign parameter to second_thing, and assign mcode0 to condition[0].
#        then_finder = re.search('>', condition[0])
#        try:
#            second_thing = condition[0][:then_finder.span()[0]]
#            condition[0] = condition[0][then_finder.span()[1]:]
#        except AttributeError:
#            raise AttributeError("> not found.")
#
#        # Turns second_thing into a class instance.
#        second_thing = self._alias(second_thing)
#
#
#        ### Redo inventory isHolding checks.
#        # @: True if thing_in_question is in second_thing, where second_thing
#        #    must be a room or an inventory (with a "holding" attribute).
#        if functional_char == '@':
#            try:
#                if thing_in_question in second_thing.holding:
#                    status = True
#                else:
#                    status = False
#            except KeyError:
#                raise AttributeError("@ error.\n"+ second_thing.name +
#                                     " has no holding attribute.")
#
#        # = : True if thing_in_question is identical with second_thing.
#        #     Generally used in conjunction with the _ alias.
#        elif functional_char == '=':
#            if thing_in_question == second_thing:
#                status = True
#            else:
#                status = False
#
#        tmp = condition if status else else_condition
#        for i in tmp: self.blueprint_main(i)
#
#        return
#
# ------------------------- Testing -----------------------------------------

def gui_init():
    F = JSON_Reader()
    F.meta_info['isCLI'] = False
    G = Game(*F.output())
    return G

if __name__ == "__main__":
    G = test_init()
    G.cliMain()
