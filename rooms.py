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
            return 'N/A'
        
    def __init__(self, r):
        self.links = [None, None, None, None]
        self.name = self.d(r, 'NA')
        self.entry_desc = self.d(r, 'EN')
        self.examine_desc = self.d(r, 'EX')
        self.reentry_desc = self.d(r, 'RE')
        self.scene_objects = [x for x in self.d(r, 'SO').split()] if (
                              self.d(r, 'SO') != '') else ['']
        self.bag_objects = [x for x in self.d(r, 'BO').split()] if (
                              self.d(r, 'BO') != '') else ['']
        self.is_visited = False
                              
    def on_entry(self):
        if self.is_visited: print(self.reentry_desc)
        else:
            print(self.entry_desc)
            self.is_visited = True
        return
    
    def __str__(self):  
        str = "Name: " + self.name + ".\n"
        str = str + "First entry message: " + self.entry_desc + "\n"
        str = str + "Reentry message: " + self.reentry_desc + "\n"
        str = str + "On examine: " + self.examine_desc + "\n"
    
        return str  
        
def room_main(room_desc, room_links = ''):
    r_d = processor(room_desc)
    r = {}
    for x in r_d.keys():
        r[x] = Room(r_d[x])
    if room_links != '': linker(room_links, r)
    return r
    
def processor(filename):
    rooms = dict()
    with open(filename) as f:
        info = f.readlines()
        for x in info:
            if '//' in x: pass
            elif '#NA' in x:
                marker = x[4:].rstrip()
                rooms[marker]=({'NA':marker})
            elif x[:3] in Room.codes.keys():
                try:
                    rooms[marker][x[1:3]] = x[4:].rstrip()
                except NameError:
                    print('No name entered; information will be ignored.')
    return rooms
    
def linker(filename, rooms):
    with open(filename) as f:
        info = f.readlines()
        for x in info:
            if '//' in x: pass
            elif x != '':
                y = x.split(', ')
                if y[0] in rooms.keys():
                    for i in range(1,5):
                        rooms[y[0]].links[i-1] = y[i].rstrip() \
                            if y[i].lower() != 'none' \
                            else None
    return
            
                        
                           
#Testing.                            
#fn = input("Enter filename: ")
'''
day = room_main('desc.txt')
for x in day:
    print(day[x])
'''