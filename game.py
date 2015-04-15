from rooms import *
from inventory import *

class Game():
    cardinals = {'w':0, 's':1, 'n':2, 'e':3}
    actions = ['throw', 'examine', 'tap', 'unlock', 'take', 'leave', 'use']
    mcode_keywords = '[+-&@!*}{^]'
    
    def __init__(self, rdata, tdata):
        self.beginning = 'Welcome to the test!' 
        self.rooms = rdata
        self.things = tdata
        self.loc = self.rooms['initial']
        self.inventory = Inventory()
        
    ''' Classes of player commands: Moving, acting, and menu. '''
    # Move: Self-explanatory, right? Uses number to set current location
    # to the room "in that direction" (specified via Room.links).
    def move(self, dir):
        try:
            self.loc = self.rooms[self.loc.links[self.cardinals[dir]]]
            self.loc.on_entry()
        except:
            print('I can\'t go that way.')
            
    # Act: Takes a command.
    def act(self, command):
        return  
    
    # Inv: Inventory menu command.
    def inv(self, command):
        return
        
    # Prompt_exe: Takes player input and passes the corresponding command
    # to the corresponding player command function.
    def prompt_exe(self, i):
        if len(i) < 1: return
        if i[0] in self.cardinals.keys():
            self.move(i)
        elif i[0] in ['west', 'south', 'north', 'east']:
            self.move(i[0][0])
        elif i[0] in self.actions:
            self.act(i)
        else:
            return
    
    ''' Functions for machine code. Includes main mcode function and ift,
        inv, obj, rom, and sys auxiliary functions as well as from tertiary 
        functions implemented by the auxiliary functions. '''
    # mcode_main: Takes a string of machine code and splits it up into pre-functional
    # character, functional character, and post-functional character.
    def mcode_main(self, words):
        type_code = words[:3]
        finder = re.search('[!]', words)
        if finder is None: raise TypeError("No functional character found.")
        
        functional_char = words[finder.span()[0]]
        target = words[4:words[finder.span()[0]]]
        parameters = words[finder.span()[1]:]
        if type_code == 'prp': type_code = 'obj'
        getattr(self, type_code+"_func")(functional_char, target, parameters)
        #print(type_code, functional_char, parameters)
        return
    
    # ift_func: Conditional mcode processor. Isolates the condition from the
    # post-functional part and enters an if-ifelse-else structure to find which
    # condition corresponds to the mcode. If true, runs each mcode line found
    # after the > (separated by }) by calling mcode_main.
    def ift_func(self, functional_char, thing_in_question, condition):
        condition = condition.split('}')
        then_finder = re.search('>', condition[0])
        second_thing = condition[0][:then_finder.span()[0]]
        condition[0] = condition[0][then_finder.span()[1]]
        if functional_char == '@':
            pass # IMPLEMENT ME!!
        return
    
    # sys_func: System mcode processor. Currently only used to print a message
    # to the terminal.
    def sys_func(self, functional_char, target, instruct):
        print("Entering system functions.")
        if functional_char == '!':
            print(instruct)
        else:
            pass
        return
    
    # inv_func: Inventory mcode processor. Used to add and remove items from the
    # inventory.
    def inv_func(functional_char, target, instruct):
        print("Entering inventory functions.")
        if functional_char == '+':
            self.inventory.add_item(target)
        elif functional_char == '-':
            self.inventory.remove_item(target)
        else:
            pass
        return
        
    # rom_func: Room mcode processor. Used to establish links, change room properties,
    # add and remove items from rooms.
    def rom_func(type, instruct):
        return

    # obj_func: Object mcode processor. Used to manipulate things.
    def obj_func(type, instruct):
        return
    
    # Tertiary function used to change the attribute of rooms and items.
    def change_var(target, attribute, new_desc):
        pointer = getattr(target, attribute) 
        new_desc = pointer
        return        
    
    # Tertiary function used to establish links between rooms.
    def link(source, dir, dest, e = True):
        if e:
            if source == dest:
                raise Error("Euclidean rooms enabled; no loops allowed.")
        source[dir] = dest
        if dir == 0: dir = 3
        elif dir == 1: dir = 2
        elif dir == 2: dir = 1
        elif dir == 3: dir = 0
        target[dir] = source
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
    
G = Game(room_processor('desc.txt','links.txt'), obj_processor('object_test.txt'))
G.main()
