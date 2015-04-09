from rooms import Room
from inventory import Thing

def file_processor(filename = ''):
    if filename = '':
        filename = input("Enter a filename: ")
    
    with open(filename) as f:
        info = f.readlines()

def room_processor(room_desc, room_links = ''):
    r_d = room_reader(room_desc)
    r = {}
    for x in r_d.keys():
        r[x] = Room(r_d[x])
    if room_links != '': link_reader(room_links, r)
    return r
    
def room_reader(filename):
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
    
def link_reader(filename, rooms):
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
    
# reads an object text file and returns a set of object dicts
def obj_reader(filename = ''):
    obj_list = []
    
    if filename == '':
        filename = input("Enter a filename: ")
    # reads the text file and creates the dictionary
    with open(filename) as f:
        info = f.readlines()
        for x in info:
            # '//' is a comment in the file
            if '//' in x: pass
            
            # NA marks an object name; creates a new object dictionary and
            # adds it to the list, marking the current working object dict
            if x[:3] == '#NA':
                marker = {'NA':x[4:].rstrip()}
                obj_list.append(marker)
                
            elif x[:3] == '#AC':
                tmp = x[4:].rstrip().split(', ')
                if 'AC' not in marker.keys():
                    marker['AC'] = {}
                marker['AC'][tmp[0]] = tmp[1:]
            elif x[:3] in Thing.codes.keys():
                try:
                    marker[x[1:3]] = x[4:].rstrip()
                except NameError:
                    print("No name entered; information discarded.")
        return obj_list
    
# takes an object metadict and returns a dict of props and a dict of items
def obj_processor(obj_list = []):
    if obj_list == []:
        obj_reader()
    props = dict()
    items = dict()
    for j in obj_list:
        x = Thing(j)
        key = x.alias
        if x.isProp:
            props[key] = x
        else:
            items[key] = x
    return props, items