import random

class Upgrade:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        
    def apply(self, player):
        raise NotImplementedError("This method should be overriden by a subclass")
    