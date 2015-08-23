from collections import OrderedDict as OrdDict

V = False # Verbose, talks about what's being done.
E = False # Error-checking, raises Exceptions if there are hiccups in JSON.

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
        
        self.zero_act = a('0').split('&') if a('0') else ['pass']

        self.unary_act = self.unaryHelper(a('1')) if a('1') else {'': ['pass']}
        self.binary_act = self.binaryHelper(a('2')) if a('2') \
                                                    else {'|': ['pass']}
                                   
        self.binary_prep = a('prep') or ''
               
        self.min, self.max = self.min_maxHelper()
        
    def unaryHelper(self, act_list):
        """ Takes a list of lists of length 2, produces an OrderedDict. """
        K = lambda x: tuple(x.split('&'))
        V = lambda y: y if type(y) is list else y.split('&')
        
        return OrdDict((K(x),V(y)) for x, y in act_list.items())
        
    def binaryHelper(self, act_list):
        """ Takes a list of lists of length 2, produces an OrderedDict. """
        def K(k):
            if '|' not in k:
                if E: raise SyntaxError("Binary conditional key missing |.")
                k = k + '|'
            k = k.split('|')
            for index, val in enumerate(k):
                k[index] = tuple(val.split('&'))
            return tuple(k)

        V = lambda y: y if type(y) is list else y.split('&')

        return OrdDict((K(x),V(y)) for x, y in act_list.items())
        
    def min_maxHelper(self):
        min, max = None, None
        
        if self.zero_act != ['pass']:
            min = 0
            max = 0
        if self.unary_act != {'':['pass']}:
            if min is None: min = 1
            max = 1
        if self.binary_act != {'|':['pass']}:
            if min is None: min = 2
            max = 2
            
        if min is None: min = -1
        if max is None: max = -1
        return min, max
    
    ''' Deprecated by Parser module implementation.
    def parseString(self, input_list):
        """ Takes a user-given list (split string) and returns a list of IDs.
        
        If fails, returns an error message. """
        val = ''
        prep_loc = 0
        
        if(input_list):
            if self.max > 0:
                if self.max > 1:
                    # try binary preposition stuff
                    try:
                        prep_loc = input_list.index(self.binary_prep)
                        val = input_list[:prep_loc] +\
                              input_list[prep_loc+1:]
                    except ValueError:
                        if self.min == 2: val = "$! Input < Min"
                        else: pass
                else: pass
                
                if not val: val = input_list[prep_loc:]
            else:
                val = "$! Input > Min"
        else:
            if self.min == 0:
                val = 0
            else:
                val = "$! 0 < Min"
        
        if V: print("Action parsed string: ", val)
        return val
    '''
    
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
        """ Takes either an Item or a tuple or Items, returns BP code. """
        if V: print("CALLING ACTION: ", input_objs)
        
        val = None        
        if (not input_objs): val = self.zero_act
        
        elif(type(input_objs) == 'tuple'): # Two objects.
            for i,j in self.binary_act:
                if self.pluralUnaryTest(input_objs[0], i) and \
                   self.pluralUnaryTest(input_objs[1], j):
                        val = self.binary_act[(i,j)]
                else: continue
                
        else: # Only one object.
            for i in self.unary_act:
                if self.pluralUnaryTest(input_objs, i):
                    val = self.unary_act[i]
                else: pass

        if V: print("Returning {}.".format(val))                
        return val or 'pass'
        
    @staticmethod    
    def action_processor(action_dict):
        """ ugh """
        actions = {}
        
        for i,j in action_dict.items():
            actions[i] = Action(j)
            
        return actions
        
