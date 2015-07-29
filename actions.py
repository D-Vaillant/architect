from collections import OrderedDict as OrdDict

V = True

class Action:
    codes = {
        "id":"id",
        "0":"zero_act",
        "1":"unary_act",
        "2":"binary_act",
        "prep":"binary_prep"
        }
        
    def __init__(self, act_dict):    
        a = lambda s: act_dict[s] if s in act_dict else None

        self.id = act_dict["id"] # id not in act_dict => something went wrong
        
        self.zero_act = a('0') or ''
        self.unary_act = self.unaryHelper(a('1') or [])
        self.binary_act = self.binaryHelper(a('2') or [])
                                   
        self.binary_prep = a('prep') or ''
               
        self.min_maxProcessor
        
    def unaryHelper(self, act_list):
        """ Takes a list of lists of length 2, produces an OrderedDict. """
        A = OrdDict()

        for x, y in act_list: # [ [x_0, y_0],...,[x_n,y_n] ]
            x = tuple(x.split('&')) #[ (xp_0, xp_1), y]
            A[x] = y
        return A 
        
    def binaryHelper(self, act_list):
        """ Takes a list of lists of length 2, produces an OrderedDict. """
        A = OrdDict()

        for x, y in act_list: # [ [x_0, y_0],...,[x_n,y_n] ]
            x = x.split("|") # [[a,b], y_0]
            for i in [0,1]:
                # [ [(ap_0,ap_1), (bp_0,bp_1)], y_0]
                x[i] = tuple(x[i].split('&')) 
            x = tuple(x) # [ ((ap_0,ap_1), (bp_0,bp_1)), y ]
            A[x] = y
        return A 
        
    def parse_string(self, input_list):
        """ Takes a user-given string and returns a list of IDs.
        
        If fails, returns an error message. """
        val = ''
        p1_loc = 0
        
        if(input_list):
            if self.max > 0:                
                if self.max > 1:
                    try:
                        p2_loc = input_list.index(self.binary_prep)
                        val = [input_list[p1_loc:p2_loc],
                               input_list[p2_loc+1:]]
                    except ValueError:
                        if self.min == 2: val = "#F:Input < 2"
                        else: pass
                else: pass
                
                val = input_list[p1_loc:]   
            else:
                val = "#F:Input > 0"
        else:
            if self.min == 0:
                val = 0
            else:
                val = "#F:0 < Max"
        
        if V: print("Action parsed string: ", val)
        return val
    
    def unaryTest(self, single_obj, condition): 
        if condition[0:2] == 'p:':
            return (condition[2:] in single_obj[0].properties)
        else:
            return (condition == single_obj[0].id) or (not condition)
            
    def pluralUnaryTest(self, single_obj, condition_array):
        for x in condition_array:
            if not self.unaryTest(single_obj, x): return False
            else: pass
        return True
    
    def call(self, input_objs):
        if V: print("CALLING ACTION: ", input_objs)
        val = None
        
        if(not input_objs): return self.dict[0]
        elif(type(input_objs) == 'tuple'): # Two objects.
            for i,j in self.dict[2]:
                if self.pluralUnaryTest(input_objs[0], i) and \
                   self.pluralUnaryTest(input_objs[1], j):
                    val = self.binary_act[(i,j)]
                else: pass
        else: # Only one object.
            for i in self.unary_act:
                if self.pluralUnaryTest(input_objs, i):
                    val = self.unary_act[i]
                else: pass
        if V: print("Returning {}.".format(val))                
            
        if V: print(val)
        return val or 'pass'
        
    @staticmethod    
    def action_processor(action_dict):
        """ ugh """
        actions = {}
        
        for i,j in action_dict.items():
            actions[i] = Action(j)
            
        return actions
        
