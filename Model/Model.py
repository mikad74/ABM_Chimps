import numpy as np
import random
from itertools import count
from Agents.Oasis import Oasis
from Agents.Crew import Chimp_crew


class Model:
    def __init__(self, n_crews, n_oases, grid_size, oasis_spawn_chance=.05):
        '''
        n_crews (int): number of initial chimp crews
        n_oases (int): number of initial oases
        grid_size(int): length of the edge of the square grid
        '''
        self.id_gen = count()
        self.grid_size = grid_size
        self.oasis_spawn_chance = oasis_spawn_chance
        self.crews = {}
        self.oases = {}
        for _ in range(n_crews):
            self.add_chimp_crew()
        for _ in range(n_oases):
            self.add_oasis()
        self.grid = []
        self.create_grid()
        self.data_track = [[], []]
        pass

    def add_chimp_crew(self, pos=None, type=None):
        """
        Generate a crew of chimps as an agent
        """
        if not pos or any(crew.pos == pos for crew in self.crews.values()):
            pos = (np.random.randint(0,self.grid_size),np.random.randint(0,self.grid_size))
            while any(crew.pos == pos for crew in self.crews.values()):
                pos = (np.random.randint(0,self.grid_size),np.random.randint(0,self.grid_size))
        id = next(self.id_gen)
        size = 1
        energy = 0
        new_crew = Chimp_crew(id, pos, size, energy, type)
        self.crews[id] = new_crew
        return new_crew

    def add_oasis(self, pos=None):
        """
        Generate a new oasis
        """
        id = next(self.id_gen)
        if not pos or any(oasis.pos == pos for oasis in self.oases.values()):
            pos = (np.random.randint(0,self.grid_size),np.random.randint(0,self.grid_size))
            while any(oasis.pos == pos for oasis in self.oases.values()):
                pos = (np.random.randint(0,self.grid_size),np.random.randint(0,self.grid_size))
        size = random.randint(2, 15)
        new_oasis = Oasis(id, pos, size)
        self.oases[id] = new_oasis
        return new_oasis
    
        
    def create_grid(self):
        grid = np.zeros((self.grid_size, self.grid_size), dtype='f')
        for crew in self.crews.values():
            grid[crew.X, crew.Y] += 1
        for oasis in self.oases.values():
            grid[oasis.X, oasis.Y] += 2
        self.grid = grid