import numpy as np
import random
from itertools import count
from Agents.Oasis import Oasis
from Agents.Crew import Chimp_crew


class Type_Model:
    def __init__(self, n_crews, n_oases, n_types, grid_size, oasis_spawn_chance=.05):
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
        for i in range(n_crews):
            self.add_chimp_crew(type=i%n_types)
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
        resource = random.randint(20, 50)
        new_oasis = Oasis(id, pos, resource)
        self.oases[id] = new_oasis
        return new_oasis
    
        
    def create_grid(self):
        grid = np.zeros((self.grid_size, self.grid_size), dtype='f')
        for crew in self.crews.values():
            grid[crew.X, crew.Y] += 1
        for oasis in self.oases.values():
            grid[oasis.X, oasis.Y] += 2
        self.grid = grid


    def run(self, cost_defeat=10, cost_fight=20, prob_win = 1/2):
        """
        Run the model for one time-step

        """


        # Remove oasis if empty TODO: Spawn new oases
        ids = []
        for oasis in self.oases.values():
            if oasis.resource <= 0:
                ids.append(oasis.id)
        for id in ids:
            del self.oases[id]
        p = random.random()
        if len(self.oases.values()) <= 3 or p <= self.oasis_spawn_chance:
            n = random.randint(0, 3)
            for _ in range(n):  self.add_oasis()



        for crew in self.crews.values(): # TODO: Randomize order??
            # Check if at oasis, if so eat, else move
            if not crew.oasis:
                

                neighboring_oases = [[],[]]
                for oasis in self.oases.values():
                    if abs(crew.X - oasis.X) <=1 and abs(crew.Y - oasis.Y) <= 1 and oasis.id not in crew.unaccessible_oases:
                        if oasis.occupied:
                            neighboring_oases[1].append(oasis.id)
                        else:
                            neighboring_oases[0].append(oasis.id)


                # Free oasis => move there
                if neighboring_oases[0]:
                    oasis = self.oases[neighboring_oases[0][0]]
                    crew.pos = (oasis.pos)
                    crew.oasis = oasis
                    oasis.occupied = True

                # Occupied oasis => Play game
                elif neighboring_oases[1]:
                    oasis = self.oases[neighboring_oases[1][0]]
                    other_crew = [crew for crew in self.crews if crew.pos == oasis.pos][0]
                    
                    if self.type == 0 or self.type < other_crew.type: # crew gets intimidated out by the defending crew
                        crew.unaccessible_oases.add(oasis)
                    
                    elif self.type == other_crew.type: # display are equal => fight
                        print("fight!")
                        if random.random() > prob_win: # crew losess
                            crew.unaccessible_oases.add(oasis) 

                        else: # crew wins
                            other_crew.oasis = None
                            other_crew.pos = crew.pos[:]
                            other_crew.unaccessible_oases.add(oasis) 
                            crew.pos = oasis.pos
                            crew.oasis = oasis

                        crew.energy -= cost_fight
                        other_crew.energy -= cost_fight
                        
                    else:
                        other_crew.oasis = None
                        other_crew.pos = crew.pos[:]
                        other_crew.unaccessible_oases.add(oasis) 
                        crew.pos = oasis.pos
                        crew.oasis = oasis

                # No oasis near, move closer to oasis
                else:
                    crew.move(self.grid_size, self.oases.values(), self.crews.values())
            else:
                crew.consume()

        self.create_grid()
        self.data_track[0].append(self.crews.values())
        self.data_track[1].append(self.oases.values())