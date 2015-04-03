from rooms import *
from room_nav import *

__author__ = "David Vaillant"

data = room_main('desc.txt', 'links.txt')

class God_Game():
    cardinals = {'w':0, 's':1, 'n':2, 'e':3}
    
    def __init__(self, data):
        self.euclid = True
        self.beginning = 'Welcome to the test!' 
        self.rooms = data
        self.loc = self.rooms['initial']
        self.link_library = {x:self.rooms[x].links for x in self.rooms}
        self.R = Room_Navigator(data)
        
    ''' It is not clear that this is necessary.    
    def update_link_library(self):
        self.link_library = {}
        for x in self.rooms:
            self.link_library[x] = self.rooms[x].links
    '''
    
    def move(self, dir):
        try:
            self.loc = self.rooms[self.loc.links[self.cardinals[dir]]]
            self.loc.on_entry()
        except:
            print('I can\'t go that way.')
   
    def main(self):
        print(self.beginning)
        prompt = ''
        while (prompt != 'q'):
            x = input('> ')
            prompt = x[0].lower() if x != '' else ''
            self.prompt_exe(prompt)
      
    def prompt_exe(self, i):
        if i in self.cardinals.keys():
            self.move(i)
        elif i == '!':
            self.god_prompter()
        else: pass
        return
        
    def god_prompter(self):
        print("Opening admin menu. Type ? for help.")
        gprompt = ''
        while (gprompt != 'q'):
            x = input('& ')
            gprompt = x[0].lower() if x != '' else ''
            self.god_prompt_exe(gprompt)
    
    def god_prompt_exe(self, i):
        if i == '?':
            print("Commands:\n Link rooms - l\n Open room navigator - r\n " +
                  "Return to game prompt - q \n ")
        elif i == 'l':
            self.create_link()
        elif i == 'r':
            self.R.main()
        else: pass
        return
    
    def create_link(self):
        dir = input('Enter a direction: ')[0]
        dir = dir[0].lower() if dir != '' else ''
        if dir not in self.cardinals.keys():
            print("Invalid direction.")
            return
        target = input('Enter the name of a room: ')
        if self.euclid:
            if target == self.loc.name:
                print("Can't connect a room to itself!")
                return
        if target in self.rooms.keys():
            self.loc.links[self.cardinals[dir]] = target
            self.link_library[self.loc.name][self.cardinals[dir]] = target
            if self.euclid:
                self.mirror(target, self.cardinals[dir])
        else:
            print("That's not the name of a room.")
        return
        
    def mirror(self, target, dir):
        if dir == 0: dir = 3
        elif dir == 1: dir = 2
        elif dir == 2: dir = 1
        elif dir == 3: dir = 0
        (self.rooms[target].links)[dir] = self.loc.name
        
    def link_printer(self, filename = ''):
        if filename == '':
            filename = input("Please enter a name for the link file: ")
        with open(filename, 'a') as f:
            for x in self.link_library.keys():
                s = x
                for y in range(4):
                    tmp = self.link_library[x][y]
                    s = s + ', ' + tmp if tmp != None else s + ', none'
                f.write(s + '\n')
        return
            
        
G = God_Game(data)
