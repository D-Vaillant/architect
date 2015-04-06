import re 

keywords = {'+', '-', '&', '%', '#', '@', '^'}

class Syntactics():
    def __init__():
        return
        
    def sem_code(self, words):
        tierI = words[:3]
        finder = re.search('[&$%^@+-]', words)
        x = finder.span()[1]
        tierII = words[x:]
        getattr(self, tierI+"_func")(type, instructions)
        return
        
    def inv_func(type, instruct):
        return
        
    def rom_func(type, instruct):

    def obj_func(type, instruct):
        
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