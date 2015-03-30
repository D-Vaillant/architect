''' rooms.py:
        Implementation of rooms for game.
        Includes a utility to translate a file into
        a dictionary of classes.
'''
__author__ = "David Vaillant"

class Room():
    codes = dict(
        {'NA':'name'},
        {'EN':'entry_desc'},
        {'RE':'reentry_desc'},
        {'EX':'examine_desc'},
        {'SO':'static_obj'}
                )
    def __init__(self):
        self.name = ''
        self.entry_desc = ''
        self.examine_desc = ''
        self.reextry_desc = ''
        self.scene_objects = []
        self.bag_objects = []
        
def processor(filename):
    rooms = dict()
    with open('filename') as f:
        info = f.readlines()
        for x in info:
            if '#NA' in x:
                rooms.append(x[:3]:{'name':x[3:]})
                marker = x[:2]
            if x[:2] in keys(rooms.codes()):
                try:
                    rooms(marker).append(rooms.codes(x[:2]):x[3:])
                except NameError:
                    print('No name entered; information will be ignored.')
    return rooms
                            
#Testing.                            
fn = input("Enter filename: ")
print(processor(fn))