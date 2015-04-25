from rooms import Room
from room_nav import Room_Navigator
from game import Game


__author__ = "David Vaillant"

class God_Game(Game):
    """ Extension of Game class. Allows use of extra commands.

    Extra commands include:
        Warping between Rooms
        Establishing links between Rooms
        Access to Room_Navigator

    Proposed extra commands:
        Access to Thing_Navigator
        Placing Things in Rooms
        Altering attributes of Rooms and Things """

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
        direct = input('Enter a direction: ')[0]
        direct = direct[0].lower() if direct != '' else ''
        if direct not in self.cardinals.keys():
            print("Invalid direction.")
            return
        target = input('Enter the name of a room: ')
        if self.euclid:
            if target == self.loc.name:
                print("Can't connect a room to itself!")
                return
        if target in self.rooms.keys():
            self.loc.links[self.cardinals[direct]] = target
            self.link_library[self.loc.name][self.cardinals[direct]] = target
            if self.euclid:
                self.mirror(target, self.cardinals[direct])
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

    def mirror(self, target, direct):
        if direct == 0: direct = 3
        elif direct == 1: direct = 2
        elif direct == 2: direct = 1
        elif direct == 3: direct = 0
        (self.rooms[target].links)[direct] = self.loc.name
        
    def link_printer(self, output_name = ''):
        """ Outputs link information into the game resource format. """

        if output_name == '':
            output_name = input("Please enter a name for the link file: ")

        with open(output_name, 'a') as f:
            s = "// Format: NAME, WEST, SOUTH, NORTH, EAST\n// " + \
                "\"none\" is used when there is nothing in a direction.\n\n"
            for x in self.link_library.keys():
                s = s + x
                for y in range(4):
                    tmp = self.link_library[x][y]
                    s = s + ' | ' + tmp if tmp != None else s + ' | none'
            f.write(s + '\n')
        return
            
