import re 
from game import Game

mcode_keywords = '[+-&@!*}{^]'


class Engine():
    def __init__(self, rdata, tdata):
        G = Game(rdata, tdata)
        return
        
    def sem_code(self, words):
        type_code = words[:3]
        finder = re.search('[!]', words)
        if finder is None: raise TypeError("No functional character found.")
        
        functional_char = words[finder.span()[0]]
        target = words[4:words[finder.span()[0]]]
        parameters = words[finder.span()[1]:]
        if type_code == 'prp': type_code = 'obj'
        getattr(self, type_code+"_func")(functional_char, target, parameters)
        #print(type_code, functional_char, parameters)
        return
    
    def ift_func(self, functional_char, thing_in_question, condition):
        condition = condition.split('}')
        then_finder = re.search('>', condition[0])
        second_thing = condition[0][:then_finder.span()[0]]
        condition[0] = condition[0][then_finder.span()[1]]
        if functional_char == '@':
            if G.
        return
    
    def sys_func(self, functional_char, target, instruct):
        print("Entering system functions.")
        if functional_char == '!':
            print(instruct)
        else:
            pass
        return
    
    def inv_func(functional_char, target, instruct):
        print("Entering inventory functions.")
        if functional_char == '+':
            G.inventory.add_item(target)
        elif functional_char == '-':
            G.inventory.remove_item(target)
        else:
            pass
        return
        
    def rom_func(type, instruct):
        return

    def obj_func(type, instruct):
        return
    
    
    def change_var(target, attribute, new_desc):
        pointer = getattr(target, attribute) 
        new_desc = pointer
        return        
        
    def link(source, dir, dest, e = True):
        if e:
            if source == dest:
                raise Error("Euclidean rooms enabled; no loops allowed.")
        source[dir] = dest
        if dir == 0: dir = 3
        elif dir == 1: dir = 2
        elif dir == 2: dir = 1
        elif dir == 3: dir = 0
        target[dir] = source
        return