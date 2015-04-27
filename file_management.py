''' file_processor.py: Contains the File_Processor class, which is run in a
        with structure and outputs an Room info dictionary and a Thing info 
        dictionary. '''

from rooms import Room
from object_source import Thing

class File_Processor():
    def __init__(self, filename = ''):
        """ Creates info and marker vars for room, thing. Takes a filename. """
        self.room_info = {}
        self.room_marker = None
        self.thing_info = {}
        self.thing_marker = None
        self.file_processor(filename)

    # Unclear if this part is necessary. Keeping anyways. 
    def __enter__(self):
        return self

    def __exit__(self, type, value, trackback):
        return

    def file_processor(self, filename = ''):
        """ Takes a filename, opens the file, and passes lines. """
        if filename == '':
            filename = input("Enter a filename: ")
        marker_dict = {'R':'room', 'L':'link', 'T':	'thing'}
        
        with open(filename) as f:
            info = f.readlines()
            marker = None
            for x in info:
                if x.isspace(): pass
                elif x[:2] == '//': pass
                elif x[0] == '~':
                    try: marker = marker_dict[x[1]]
                    except KeyError: raise KeyError("Invalid marker line.")
                elif marker == None:
                    raise Exception("No marker specified.")
                else:
                    getattr(self, marker+"_reader")(x)

        
    def room_reader(self, line):
        """ Reads a line of text and alters room_* attributes accordingly.

        On name specification:
            Adds a new Room dictionary to room_info, sets room_marker
            to its key. 

        On property specification:
            Adds a new entry to the marked Room dictionary. 

        Otherwise: prints a warning and continues. """	

        # NA marks a Room name; creates a new Room dictionary and adds it to
        # room_info. room_marker is set to the current working Room name.
        if '#NA' in line:
            self.room_marker = line[4:].rstrip()
            self.room_info[self.room_marker]=({'NA':self.room_marker})
        elif '#EN' in line or '#EX' in line or '#RE' in line:
            try:
                target = self.room_info[self.room_marker]
            except KeyError:
                print("No room name entered; information will be ignored.")
            
            try:
                target[line[1:3]] += ("\n" + line[4:].rstrip())
            except KeyError:
                target[line[1:3]] = line[4:].rstrip()
                
        # For other properties of Rooms, strips away whitespace and adds it to
        # the Room dictionary.
        elif line[:3] in Room.codes.keys():
            try:
                self.room_info[self.room_marker][line[1:3]] = line[4:].rstrip()
            except NameError:
                print('No room name entered; information will be ignored.')
        else: print('WARNING - Invalid entry: ' + line)
        return
        
    def link_reader(self, line):
        """ Takes a line marked as \'link\', alters room[\'L\'] accordingly.

        Warns if specified room dictionary is not found. """
        y = line.rstrip().split(' | ')
        try:
            self.room_info[y[0]]['L'] = [y[i+1].rstrip() if y[i+1].lower() != 'none'
                                            else None for i in range(4)]
        except KeyError:
                print("WARNING - Attempted to set links for an unknown room.")
                print("Line: "+ line)
        return

    def thing_reader(self, line):
        """ Reads a line of text and alters thing_* attributes accordingly.

        On name specification:
            Adds a new Thing dictionary to thing_info, 
            sets thing_marker to its key.

        On property specification:
            Adds a new entry to the marked Thing dictionary.

        Otherwise: prints a warning and continues. """

        # NA marks a Thing name; creates a new Thing dictionary and
        # adds it to thing_info. thing_marker is set to the current
        # working Thing name.
        if line[:3] == '#NA':
            self.thing_marker = line[4:].rstrip()
            self.thing_info[self.thing_marker] = {'NA':self.thing_marker}
            
        # For actions: machine codes are separated by '{'.
        # Creates a list tmp; tmp[0] is the action name.
        elif line[:3] == '#AC':
            # Use { to split up various parts of the plaintext into
            # individual mcode commands.
            tmp = line[4:].rstrip().split('{')
            
            # Creates an empty dict if this is the first action.
            if 'AC' not in self.thing_info[self.thing_marker].keys():
                self.thing_info[self.thing_marker]['AC'] = {}
            # Add associated machine code to action dictionary.
            self.thing_info[self.thing_marker]['AC'][tmp[0]] = tmp[1:]
            
        # For other properties, strip away trailing whitespace and 
        # add property code : property description to object dictionary.
        elif line[:3] in Thing.codes.keys():
            try:
                self.thing_info[self.thing_marker][line[1:3]] = line[4:].rstrip()
            # If no name has been entered before a property, raise Error.
            except NameError:
                print("No name entered; information discarded.")
        return
        
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
