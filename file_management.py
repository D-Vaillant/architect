''' file_processor.py: Contains the File_Processor class, which is run in a
        with structure and outputs an Room info dictionary and a Thing info 
        dictionary. '''

from rooms import Room
from object_source import Thing
from collections import OrderedDict as OrdDict

V = False

class File_Processor():

    marker_dict = {'A':'action', 'R':'room', 'M':'meta',
                   'L':'link', 'T':'thing'}
                   
    def __init__(self, filename = '', ut = False):
        """ Creates info and marker vars for room, thing. Takes a filename. """
        self.room_info = {}
        self.room_marker = None
        self.thing_info = {}
        self.thing_marker = None
        self.action_info = {}
        self.action_marker = None
        self.meta_info = {}
        self.meta_marker = None
        
        self.unitTesting = ut
        self.file_processor(filename)        

    # Unclear if this part is necessary. Keeping anyways. 
    def __enter__(self):
        return self

    def __exit__(self, type, value, trackback):
        return

    def file_processor(self, filename):
        """ Takes a filename, opens the file, and passes lines. 
        
            If unitTesting, does other things. """
            
        if filename == '':
            filename = input("Enter a filename: ")
        
        if self.unitTesting: self.file_reader(filename)
        else:
            
            with open(filename) as f:
                self.file_reader(f)

    def file_reader(self, f):
        marker = None

        # Iterates over the lines of the file.
        for x in f.readlines():
            if V: print(x)
            if self.unitTesting: x = x.decode('UTF-8')
            
            # Skips comments and blank lines.
            if x.isspace(): pass
            elif x[:2] == '//': pass
            
            # ~ delineates different regions.
            elif x[0] == '~':
                try: marker = self.marker_dict[x[1]]
                except KeyError: raise KeyError("Invalid marker line.")
                
            # Raises error if non-skipped, non-marker line occurs before
            # a marker has been set.
            elif marker == None:
                raise Exception("No marker specified.")
            
            # Uses marker to decide which reader to pass line to.
            else:
                getattr(self, marker+"_reader")(x.rstrip())
    
    def action_reader(self, line):
        """ Does action reading things. """
        
        # The # symbol marks a new action.
        if line[0] == '#':
            self.action_marker = line[1:].rstrip()
            self.action_info[self.action_marker]={0:'', 1:OrdDict(),
                                                        2:OrdDict()}
        
        # ! marks a preposition; !1 or !2
        elif line[0] == '!':
            if line[1] in ['1', '2']:
                self.action_info[self.action_marker]['P'+line[1]] = \
                                                    line[3:]
            else:
                print("Failed at adding a preposition: " + line)
        
        # V sets "unaryVerbose" to True; makes unary preposition non-optional
        elif line[0] == 'V':
            self.action_info[self.action_marker]['V'] = True
                
        # / marks a line of form objects/bp_code.
        elif "/" in line:
            try:
                # tmp0 = objects, tmp1 = bp_code.
                tmp0, tmp1 = line.split("/")
                
                # tmp1 turned into an array of individual bp_code lines.
                tmp1 = tmp1.split("|")
                
                # if tmp0 is 0, bp_code corresponds to action without objs.
                if tmp0 == '0':
                    self.action_info[self.action_marker][0]=tmp1
                    
                # if tmp0 has a |, split it into a binary spec
                elif "|" in tmp0:
                    try:
                        obj0, obj1 = tmp0.split("|")
                        obj0 = tuple(obj0.split('&'))
                        obj1 = tuple(obj1.split('&'))
                        self.action_info[self.action_marker][2][(obj0,obj1)]\
                            = tmp1
                    except ValueError:
                        print("Something went wrong with the | split: " + line)
                
                # Otherwise tmp0 is a unary spec.
                # & divides up different requirements, eg multiple properties.
                else:
                    self.action_info[self.action_marker][1]\
                                    [tuple(tmp0.split('&'))] = tmp1
            except ValueError:
                print("Too many /'s found: " + line)
        else:
            print("Warning - Invalid entry: " + line)
                    
    def room_reader(self, line):
        """ Reads a line of text and alters room_* attributes accordingly.

        On name specification:
            Adds a new Room dictionary to room_info, sets room_marker
            to its key. 

        On property specification:
            Adds a new entry to the marked Room dictionary. 

        Otherwise: prints a warning and continues. """	

        # IDEN marks a Room ID; creates a new Room dictionary and adds it to
        # room_info. room_marker is set to the current working Room name.
        if '#IDEN' in line:
            self.room_marker = line[6:]
            self.room_info[self.room_marker]=({'IDEN':self.room_marker})
            
        # Entry, examine, and re-entry are all multi-line properties.
        elif '#DESC' in line:
            try:
                target = self.room_info[self.room_marker]
            except KeyError:
                print("No room name entered; information will be ignored.")
            
            try:
                target[line[1:5]] += ("\n" + line[6:])
            except KeyError:
                target[line[1:5]] = line[6:]
                
        # For other properties of Rooms, strips away whitespace and adds it to
        # the Room dictionary.
        elif line[:5] in Room.codes.keys():
            try:
                self.room_info[self.room_marker][line[1:5]] = line[6:]
            except NameError:
                print("No room name entered; information will be ignored.")
                
        else: print("WARNING - Invalid Room entry: " + line)
        return
        
    def link_reader(self, line):
        """ Takes a line marked as 'link', alters room['L'] accordingly.

        Warns if specified room dictionary is not found. 
        Room_Reader must be run first. """
        
        # Splits line into [ROOM_BEING_LINKED, R,R,R,R] form.
        y = line.split(' | ')
        try:
            self.room_info[y[0]]['L'] = [y[i] if y[i].lower() != 'none'
                                              else None for i in range(1,5)]
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

        # IDEN marks a Thing ID; creates a new Thing dictionary and
        # adds it to thing_info. thing_marker is set to the current
        # working Thing name.
        if line[:5] == '#IDEN':
            self.thing_marker = line[6:]
            self.thing_info[self.thing_marker] = {'IDEN':self.thing_marker}
         
        # For other properties, strip away trailing whitespace and 
        # add property code : property description to object dictionary.
        elif line[:5] in Thing.codes.keys():
            try:
                self.thing_info[self.thing_marker][line[1:5]] = line[6:]
            # If no ID has been entered before a property, raise Error.
            except NameError:
                print("No ID entered; information discarded.")
        return
    
    # Deprecated by new action system.
    """
    elif line[:3] == '#AC':
        # Use { to split up various parts of the plaintext into
        # individual mcode commands.
        tmp = line[4:].split('{')
        
        # Creates an empty dict if this is the first action.
        if 'AC' not in self.thing_info[self.thing_marker].keys():
            self.thing_info[self.thing_marker]['AC'] = {}
        # Add associated machine code to action dictionary.
        self.thing_info[self.thing_marker]['AC'][tmp[0]] = tmp[1:]
    """
        
    # Deprecated by staticmethods in Thing class.
    """
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
    """
