
import numpy as np
import random
from itertools import count
from Agents.Oasis import Oasis
from Agents.Crew import Chimp_crew


class Model:
    def __init__(self, n_crews, n_oases, grid_size, oasis_spawn_proportional=False, avg_oasis_size=100, abundance_factor=20, crew_consumption_rate=1,):
        '''
        n_crews (int): number of initial chimp crews
        n_oases (int): number of initial oases
        grid_size(int): length of the edge of the square grid
        '''
        self.id_gen = count()
        self.grid_size = grid_size
        self.oasis_spawn_proportional = oasis_spawn_proportional
        self.avg_oasis_size = avg_oasis_size
        self.abundance_factor = abundance_factor
        self.crew_consumption_rate = crew_consumption_rate
        self.crews = {}
        self.oases = {}
        for _ in range(n_crews):
            self.add_chimp_crew()
        self.update_oases
        # for _ in range(n_oases):
        #     self.add_oasis(random.gauss(avg_oasis_size, avg_oasis_size*0.1))
        self.grid = []
        self.create_grid()
        self.data_track = [[], []]
        pass

    def add_chimp_crew(self, pos=None):
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
        new_crew = Chimp_crew(id, pos, size, energy)
        self.crews[id] = new_crew
        return new_crew

    def update_oases(self):
        # delete empty oases
        ids = []
        for oasis in self.oases.values():
            if oasis.resource <= 0:
                ids.append(oasis.id)
        for id in ids:
            del self.oases[id]

        if self.oasis_spawn_proportional:
            oasis_spawn_factor = len(self.crews)
        else:
            oasis_spawn_factor = self.n_crews

        current_food = sum([oasis.resource for oasis in self.oases.values()])
        food_required = oasis_spawn_factor * self.abundance_factor * self.crew_consumption_rate - current_food
        oases_required = int(-(food_required // -self.avg_oasis_size))
        for _ in range(oases_required):
            self.add_oasis(random.gauss(self.avg_oasis_size, self.avg_oasis_size/3))


    def add_oasis(self, size, pos=None):
        """
        Generate a new oasis
        """
        id = next(self.id_gen)
        if not pos or any(oasis.pos == pos for oasis in self.oases.values()):
            pos = (np.random.randint(0,self.grid_size),np.random.randint(0,self.grid_size))
            while any(oasis.pos == pos for oasis in self.oases.values()):
                pos = (np.random.randint(0,self.grid_size),np.random.randint(0,self.grid_size))
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
        

