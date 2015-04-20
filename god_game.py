from rooms import Room
from room_nav import Room_Navigator
from game import Game


__author__ = "David Vaillant"

data = room_processor('testgame_desc.txt')

class God_Game(Game):
    ''' Extension of Game class. Allows on-the-fly creation of links between
        rooms and general testing of the data file loaded. ''' 

    def __init__(self, rdata, tdata):
        self.euclid = True
        super(God_Game, self).__init__(rdata, tdata)
        self.link_library = {x:self.rooms[x].links for x in self.rooms}
        self.R = Room_Navigator(data)
      
    def prompt_exe(self, i):
        if len(i) < 1: return
        elif i == '!':
            self.god_prompter()
        else:
            super().prompt_exe(i)
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
        elif i == 'l': self.create_link()
        elif i == 'w': self.warp()
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
        
    def warp(self):
        dest = input('Enter a room name: ')
        if dest not in self.rooms.keys():
            print("Room not found.")
            return
        else:
            self.loc = self.rooms[dest]
            self.loc.on_entry()
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
            s = "// Format: NAME, WEST, SOUTH, NORTH, EAST\n// " + \
                "\"none\" is used when there is nothing in a direction.\n\n"
            for x in self.link_library.keys():
                s = s + x
                for y in range(4):
                    tmp = self.link_library[x][y]
                    s = s + ', ' + tmp if tmp != None else s + ', none'
            f.write(s + '\n')
        return
            
        
G = God_Game(data)
