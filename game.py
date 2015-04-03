from rooms import *

class Game():
    cardinals = {'w':0, 's':1, 'n':2, 'e':3}

    
    def __init__(self, data):
        self.beginning = 'Welcome to the test!' 
        self.rooms = data
        self.loc = self.rooms['initial']
        
    def move(self, dir):
        try:
            self.loc = self.rooms[self.loc.links[self.cardinals[dir]]]
            self.loc.on_entry()
        except:
            print('I can\'t go that way.')
        
    def prompt_exe(self, i):
        if i in self.cardinals.keys():
            self.move(i)
        else:
            return
    
    def main(self):
        print(self.beginning)
        prompt = ''
        while (prompt != 'q'):
            x = input('> ')
            prompt = x[0].lower() if x != '' else ''
            self.prompt_exe(prompt)
    
    
G = Game(room_main('desc.txt','links.txt'))
G.main()