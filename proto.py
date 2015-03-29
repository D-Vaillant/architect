#from INPUT import choice

class Room():
    def __init__(self):
        self.name = ''
        self.entry_desc = ''
        self.examine_desc = ''
        self.reextry_desc = ''
        self.scene_objects = []
        self.bag_objects = []
        
class Game():
    def __init__(self):
        self.state = 'initial'
        self.loc = 'begin'
        
    def update(self)
        
def main():
    G = Game()
    while(G.state != 'quit'):
        G.state = choice()
        G.update
    