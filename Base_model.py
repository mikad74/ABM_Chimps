import numpy as np

class Model:
    def __init__(self, n_crews, n_oases):
        self.crews = [self.add_chimpcrew() for n  in range(n_crews)]
        self.oases = [self.add_oasis() for n in range(n_oases)]
        pass

    def add_chimp_crew(self):
        pos = (0,0)             #TODO: adjust attributes of crew
        size = 0
        energy = 0
        new_crew = Chimp_crew(pos, size, energy)
        return new_crew
        # track chimps
        # track oases

    def add_oasis(self):
        pos = (0,0)
        size = 0
        new_oasis = Oasis(pos, size)
        return 0
    
    def run(self):
        for crew in self.crews:
            pass # move

        return 0 
        

class Chimp_crew:
    def __init__(self, pos, crew_size=10, initial_energy=100):
        self.crew_size = crew_size # size of crew
        self.pos = pos # position of the crew on the spatial domain
        self.energy = initial_energy # energy of our crew: goes up when the crew is currently occupying a resource rich oasis, goes down whem the crew moves, fights
        self.nomad = True # whether the crew is currently looking for a new source of food

    def intimidate(self, other_crew, oasis, cost_fight = 20, cost_loss = 10):
        '''
        this function returns the valuation that a crew assigns to a ressource (benefit) depending on how
        hard it might be to take it over (cost)
        '''
        
        pre_utility = [[oasis.ressource - cost_fight, oasis.ressource], [-cost_fight - cost_loss, - cost_loss]] # potential outcomes from a conflict
        # look for equilibrium here


    def step(self):
        pass
        # motion
        # check for neighboring oases
        # check for oasis status


class Oasis:
    def __init__(self, pos, ressource):
        self.pos = pos
        self.ressource = ressource
        self.occupied = False