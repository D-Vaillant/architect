from collections import OrderedDict as OrdDict

V = True

class Action:
    def __init__(self, act_dict):        
        self.dict = {x:act_dict[x] for x in act_dict 
                                   if x in [0,1,2] and act_dict[x]}
                                   
        a = lambda s: act_dict[s] if s in act_dict else ''                   
        self.unary_prep = a('P1')
        self.binary_prep = a('P2')
        
        ## self.unaryVerbose = 'V' in act_dict
        
        self.min = min(self.dict)
        self.max = max(self.dict)
        
        
    def parse_string(self, input_list):
        """ Takes a user-given string and returns a list of IDs.
        
        If fails, returns an error message. """
        val = ''
        p1_loc = 0
        
        if(input_list):
            if self.max > 0:
                if input_list[0] == self.unary_prep:
                    p1_loc += 1
                ## else:
                ##     if self.unaryVerbose:
                ##         return "FAIL: No unary prep."
                ##     else: pass 
                
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
                    val = self.dict[2][(i,j)]
                else: pass
        else: # Only one object.
            for i in self.dict[1]:
                if self.pluralUnaryTest(input_objs, i):
                    val = self.dict[1][i]
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
        
