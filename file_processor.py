from rooms import Room
from inventory import Thing

class File_Processor():
    def __init__(filename = ''):
        self.file_loc = filename

    def __enter__(self):
        
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
    
    
def obj_reader(filename = ''):
''' reads an object text file and returns a set of object dicts '''

    # default behavior: prompt user for file location
    if filename == '':
        filename = input("Enter a filename: ")

    obj_list = []
    
    # reads the text file and creates the dictionary
    with open(filename) as f:
        info = f.readlines()
        for x in info:
            # '//' is a comment in the file
            if '//' in x: pass
            
            # NA marks an object name; creates a new object dictionary and
            # adds it to the set, marking the current working object dict
            if x[:3] == '#NA':
                marker = {'NA':x[4:].rstrip()}
                obj_list.append(marker)
                
            # For actions: machine codes are separated by '{'.
            # Creates a list tmp; tmp[0] is the action name.
            elif x[:3] == '#AC':
                # Use { to split up various parts of the plaintext into
                # individual mcode commands.
                tmp = x[4:].rstrip().split('{')
                
                # Creates an empty dict if this is the first action.
                if 'AC' not in marker.keys():
                    marker['AC'] = {}
                # Add associated machine code to action dictionary.
                marker['AC'][tmp[0]] = tmp[1:]
                
            # For other properties, strip away trailing whitespace and 
            # add property code : property description to object dictionary.
            elif x[:3] in Thing.codes.keys():
                try:
                    marker[x[1:3]] = x[4:].rstrip()
                # If no name has been entered before a property, raise Error.
                except NameError:
                    print("No name entered; information discarded.")
        return obj_list
    
# takes an object metadict and returns a dict of props and a dict of items
def obj_processor(obj_list = []):
    if obj_list == []:
        obj_reader()
    if type(obj_list) == str:
        obj_list = obj_reader(obj_list)

    things = dict()
    obj_list = obj_putter(obj_list)
     
    # iterates over 
    for j in obj_list:
        x = Thing(j)
        key = x.name
        things[key] = x
    return things
    
def obj_putter(fileIn = '', fileOut = ''):
    sourceList = obj_reader(fileIn) if type(fileIn) is str else fileIn
    for ele in sourceList:
        for code in Thing.codes:
            if code[1:] not in ele.keys():
                ele[code[1:]] = {} if code == '#AC' \
                                else 'pass'
    if fileOut != '':
        with open(fileOut, 'a') as f:
            pass
            # write the object file properly. unimplemented
    return sourceList
