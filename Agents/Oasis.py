from .Base import Agent


class Oasis(Agent):
    def __init__(self, id, pos, resource):
        self.id = id
        self.pos = pos
        self.resource = resource
        self.occupied = False
    
    def get_consumed(self, amount):
        food = min(amount, self.resource)
        self.resource -= food
        return food, self.resource