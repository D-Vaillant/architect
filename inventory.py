from collections import defaultdict
__author__ = "David Vaillant"

class Inventory():
    def passer():
        return 'pass'

    def __init__(self):
        self.collection = {}
        
    def add_item(self, x):
        if x not in self.collection.keys():
            self.collection[x] = 1
        else:
            self.collection[x] += 1
        return
        
    def remove_item(self, x):
        if x in self.collection.keys():
            self.collection[x] = max(x-1, 0)
        else:
            print("Warning: Trying to remove a non-existent object.")
            return
            
class Thing():
    codes = {
        '#NA':'name',
        '#EX':'examine_desc',
        '#OA':'on_acquire',
        '#AC':'action',
        '#TY':'type',
        '#AL':'alias',
        '#GD':'ground_desc'
        }
    def __init__(self, itemD):
        self.name = itemD['NA']
        self.alias = itemD['AL']
        self.examine_desc = itemD['EX']
        self.ground_desc = itemD['GD']
        self.on_acquire = itemD['OA']
        self.action_dict = {act:mcode for act, mcode in itemD['AC'].items()}
        self.isProp = True if itemD['TY'] == 'prop' else False
        
       
    
# reads an object text file and returns a set of object dicts
def obj_reader(filename = ''):
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
                tmp = x[4:].rstrip().split('{')
                
                # Creates an empty dict if this is the first action.
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
    if type(obj_list) == str:
        obj_list = obj_reader(obj_list)
        
    props = dict()
    items = dict()
    obj_list = obj_putter(obj_list)
     
    # iterates over 
    for j in obj_list:
        x = Thing(j)
        key = x.name
        if x.isProp:
            props[key] = x
        else:
            items[key] = x
    return props, items
    
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
            

    