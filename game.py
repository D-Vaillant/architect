from rooms import *
from inventory import *
from collections import Counter

class Game():
    cardinals = {'w':0, 's':1, 'n':2, 'e':3}
    actions = ['throw', 'examine', 'tap', 'unlock', 'take', 'leave', 'use']
    
    
    def __init__(self, rdata, tdata):
        self.beginning = 'Welcome to the test!' 
        self.rooms = rdata
        self.props = tdata[0]
        self.items = tdata[1]
        self.inventory = Counter()
        self.loc = self.rooms['initial']
        self.inventory = Inventory()
        
    def move(self, dir):
        try:
            self.loc = self.rooms[self.loc.links[self.cardinals[dir]]]
            self.loc.on_entry()
        except:
            print('I can\'t go that way.')
            
    def act(self, command):
        return  
    
    def inv(self, command):
        return
        
        
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
    
    def main(self):
        print(self.beginning)
        prompt = ' '
        while (prompt[0] != 'q' and prompt[0] != 'quit'):
            x = input('> ')
            prompt = x.lower().split() if x != '' else ''
            if prompt == []: prompt = ' '
            self.prompt_exe(prompt)
        raise NameError("Game finished.")
    
    
G = Game(room_processor('desc.txt','links.txt'), obj_processor('object_test.txt'))
G.main()
