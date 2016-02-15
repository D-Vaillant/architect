""" event.py
        Test module for Event class for Architect. 
        
    """
    
class Event:
    def __init__(self, id,
                       payload = "pass",
                       prewhispers = "none"):
        self.id = id
        self.payload = payload
        self.prewhispers = prewhispers
        
    def trigger(self):
        return payload
        