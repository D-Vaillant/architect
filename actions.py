from collections import OrderedDict as OrdDict

V = True  # Verbose, talks about what's being done.
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
        self.isKnown = a('isKnown') or True

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
        if self.binary_act != {('',''):['pass']}:
            if min is None: min = 2
            max = 2

        if min is None: min = -1
        if max is None: max = -1
        return min, max

    @staticmethod
    def unaryTest(item, condition):
        """ Tests if item fulfills the given condition. """
        if V: print("Testing condition: {}".format(condition))
        
        is_negated = (condition[0] == '~')
        if condition[:2] == 'p:':
            val = (condition[2:] in item.properties)
        else:
            val = (condition == item.id) or (not condition)
        return (not val) if is_negated else val
    
    @staticmethod
    def pluralUnaryTest(single_obj, condition_array):
        for x in condition_array:
            if Action.unaryTest(single_obj, x): continue 
            else: return False
        return True

    def call(self, input_objs):
        """ Takes either an Item or a tuple or Items, returns BP code. """
        val = None
        if input_objs == 0:
            val = self.zero_act

        elif(len(input_objs) == 2):
            for (i,j),bp in self.binary_act.items():
                if self.pluralUnaryTest(input_objs[0], i) and \
                   self.pluralUnaryTest(input_objs[1], j):
                        val = bp 
                        break
                else: continue

        else: # Only one object.
            for i,bp in self.unary_act.items():
                if self.pluralUnaryTest(input_objs[0], i):
                    val = bp 
                    break
                else: continue

        if V: print("Returning {}.".format(val))
        return val or 'pass'

    @staticmethod
    def action_processor(action_dict):
        """ ugh """
        actions = {}

        for i,j in action_dict.items():
            actions[i] = Action(j)

        return actions

