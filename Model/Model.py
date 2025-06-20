import numpy as np
import random
from itertools import count
from Agents.Oasis import Oasis
from Agents.Crew import Chimp_crew


class Model:
    def __init__(self, n_crews,  grid_size, oasis_spawn_proportional=False, abundance_factor=20, oasis_density=0.24, initialise_crews=True, food_consumption_speed=2, crew_energy_expenditure=1):
        '''
        n_crews (int): number of initial chimp crews
        n_oases (int): number of initial oases
        grid_size(int): length of the edge of the square grid
        '''
        self.id_gen = count()
        self.n_crews = n_crews
        self.grid_size = grid_size
        self.oasis_spawn_proportional = oasis_spawn_proportional
        self.abundance_factor = abundance_factor
        self.crew_energy_expenditure = crew_energy_expenditure
        self.crew_consumption_rate = food_consumption_speed * 2 * np.sqrt(oasis_density)
        self.crews = {}
        self.oases = {}
        if initialise_crews: 
            self.initial_n_chimps = self.initialize_crews()
            self.avg_oasis_size = self.food_required / (oasis_density * grid_size * grid_size )
            self.update_oases()
        self.grid = []
        self.create_grid()
        self.data_track = [[], []]



    @property
    def food_required(self):
        if self.oasis_spawn_proportional:
            oasis_spawn_factor = self.n_chimps
        else:
            oasis_spawn_factor = self.initial_n_chimps

        current_food = sum([oasis.resource for oasis in self.oases.values()])
        food_required = oasis_spawn_factor * self.abundance_factor * self.crew_energy_expenditure - current_food
        return food_required

    @property
    def n_chimps(self):
        return sum([crew.crew_size for crew in self.crews.values()])

    def initialize_crews(self):
        for _ in range(self.n_crews):
            self.add_chimp_crew()
        return self.n_chimps

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
        new_crew = Chimp_crew(id, pos, size, energy, type, consumption_rate=self.crew_consumption_rate, expenditure=self.crew_energy_expenditure)
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

        oases_required = int(-(self.food_required // -self.avg_oasis_size))
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