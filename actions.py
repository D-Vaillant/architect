class Action:
    def __init__(self, act_dict):
        self.dict = {x:act_dict[x] for x in act_dict if act_dict[x]}
        self.unary_prep = act_dict["P1"] if 'P1' in act_dict else ''
        self.binary_prep = act_dict["P2"] if 'P2' in act_dict else ''
        self.unaryVerbose = 'V' in act_dict
        self.min = min(self.dict)
        self.max = max(self.dict)
        
        
    def call_action(input_string):
        self._conditional_worker(input_string.split("/"))
        return 
        
    