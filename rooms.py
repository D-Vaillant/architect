''' rooms.py:
        Implementation of rooms for game.
        Includes a utility to translate a file into
        a dictionary of classes.
'''
__author__ = "David Vaillant"

class Room():
    codes = {
        '#NA':'name',
        '#EN':'entry_desc',
        '#RE':'reentry_desc',
        '#EX':'examine_desc',
        '#SO':'static_obj',
        '#BO':'bag_obj'
            }
    def d(self, room_dict, i):
        try:
            return room_dict[i]
        except:
            return None
        
    def __init__(self, r):
        self.links = [None, None, None, None]
        self.name = self.d(r, 'NA')
        self.entry_desc = self.d(r, 'EN')
        self.examine_desc = self.d(r, 'EX')
        self.reentry_desc = self.d(r, 'RE')
        self.scene_objects = [x for x in self.d(r, 'SO').split()] if (
                              self.d(r, 'SO') != None) else None
        self.bag_objects = [x for x in self.d(r, 'BO').split()] if (
                              self.d(r, 'BO') != None) else None

    def __str__(self):
        # Here I write some return statement which gives what I want it to give.
        
def processor(filename):
    rooms = dict()
    with open(filename) as f:
        info = f.readlines()
        for x in info:
            if '#NA' in x:
                marker = x[4:].rstrip()
                rooms[marker]=({'NA':marker})
            if x[:3] in Room.codes.keys():
                try:
                    rooms[marker][x[1:3]] = x[4:].rstrip()
                except NameError:
                    print('No name entered; information will be ignored.')
    return rooms
    
def linker(filename, rooms):
    with open(filename) as f:
        info = f.readlines()
        for x in info:
            y = x.split('')
            for i in range(1,len(y)):
                rooms(y[0]).links[i] = i.rstrip() if i != 'None' else None
    return
            
                        
                           
#Testing.                            
#fn = input("Enter filename: ")
print(processor('test.txt'))
