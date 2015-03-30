

class Game():
    def __init__(self, data):
        self.rooms = data
        self.loc = self.rooms['initial']
        
    def update(self):
    