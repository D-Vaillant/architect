from rooms import *
from collections import Counter

class Game():
    cardinals = {'w':0, 's':1, 'n':2, 'e':3}
    actions = ['throw', 'examine', 'tap', 'unlock', 'take', 'leave', 'use']
    
    
    def __init__(self, rdata, tdata):
        self.beginning = 'Welcome to the test!' 
        self.rooms = rdata
        self.props = tdata['props']
        self.items = tdata['items']
        self.loc = self.rooms['initial']
        
    def move(self, dir):
        try:
            self.loc = self.rooms[self.loc.links[self.cardinals[dir]]]
            self.loc.on_entry()
        except:
            print('I can\'t go that way.')
            
    def act(self, command):
        
    
    def inv(self, command)
        
        
    def prompt_exe(self, i):
        if i[0] in self.cardinals.keys():
            self.move(i)
        elif i[0] in ['west', 'south', 'north', 'east']:
            self.move(i[0][0])
        elif i[0] in self.actions.keys():
            self.act(i)
        else:
            return
    
    def main(self):
        print(self.beginning)
        prompt = ''
        while (prompt != 'q'):
            x = input('> ')
            prompt = x.lower().split() if x != '' else ''
            self.prompt_exe(prompt)
    
    
G = Game(room_main('desc.txt','links.txt'))
G.main()
