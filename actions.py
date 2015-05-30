from collections import OrderedDict as OrdDict

class Action:
    def __init__(self, act_dict):
        self.dict = {x:act_dict[x] for x in act_dict 
                                   if x in [0,1,2] and act_dict[x]}
        self.unary_prep = act_dict["P1"] if 'P1' in act_dict else ''
        self.binary_prep = act_dict["P2"] if 'P2' in act_dict else ''
        self.unaryVerbose = 'V' in act_dict
        
        self.min = min(self.dict)
        self.max = max(self.dict)
        
        
    def parse_string(self, input_list):
        p1_loc = 0
        if(input_list):
            if self.max > 0:
                if input_list[0] == self.unary_prep:
                    p1_loc += 1
                    
                # Optional, depending on desired input strictness.
                """
                else:
                    if self.unaryVerbose:
                        return "FAIL: No unary prep."
                    else: pass 
                """
                
                if self.max > 1:
                    try:
                        p2_loc = input_list.index(self.binary_prep)
                        return [input_list[p1_loc:p2_loc],
                                input_list[p2_loc+1:]]
                    except ValueError:
                        if self.min == 2: return "#F:Input < 2"
                        else: pass
                else: pass
                
                return input_list[p1_loc:]   
            else:
                return "#F:Input > 0"
        else:
            if self.min == 0:
                return 0
            else:
                return "#F:0 < Max"
    
    def unaryTest(self, single_obj, condition): 
        if condition[0:2] == 'p:':
            return (condition[2:] in single_obj[0].properties)
        else:
            return (condition == single_obj[0].alias) or (not condition)
    
    def call_action(self, input_objs):
        if(not input_objs): return self.dict[0]
        elif(type(input_objs) == 'tuple'): # Two objects.
            for i,j in self.dict[2]:
                if self.unaryTest(input_objs[0], i) and \
                   self.unaryTest(input_objs[1], j):
                    return self.dict[2][(i,j)]
                else: pass
        else: # Only one object.
            for i in self.dict[1]:
                if self.unaryTest(input_objs, i):
                    return self.dict[1][i]
                else: pass
        raise KeyError("Missing default case!")
                
            
        return 'pass'
        
        
    def action_processor(action_dict):
        """ ugh """
        actions = {}
        
        for i,j in action_dict.items():
            actions[i] = Action(j)
            
        return actions
        
    