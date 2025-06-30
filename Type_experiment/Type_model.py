import numpy as np
import random
from itertools import count
import sys
import os


# Add ABM_Chimps to the path manually
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from Agents.Oasis import Oasis
from Agents.Crew import Chimp_crew

class Type_Chimp_crew(Chimp_crew):
    def __init__(self, id, pos, crew_size=10, initial_energy=100, strat=None, ram = 5):
        super().__init__(id, pos, crew_size, initial_energy)
        self.strat = strat
        self.type = None
        self.last_opp_type = -1
        self.recent_history = [0 for _ in range(ram)]

class Type_Model:
    def __init__(self, n_crews, n_oases, n_types, grid_size, resource_per_oasis = 150, cost_fight = 10, resource_constant = 100, seasons = False, flexible = 2, ram = 5):
        '''
        n_crews (int): number of initial chimp crews
        n_oases (int): number of initial oases
        grid_size(int): length of the edge of the square grid
        '''
        self.seasons = seasons
        self.flex = flexible
        self.ram = ram
        self.resource_constant = resource_constant
        self.id_gen = count()
        self.grid_size = grid_size
        self.n_crews = n_crews
        self.resource = resource_per_oasis
        self.crews = {}
        self.oases = {}
        for i in range(n_crews):
            self.add_chimp_crew(strat=i%n_types)
        for _ in range(n_oases):
            self.add_oasis()
        self.grid = []
        self.create_grid()
        self.data_track = [[], []]
        self.cost_fight = cost_fight
        pass

    def add_chimp_crew(self, pos=None, strat=None):
        """
        Generate a crew of chimps as an agent
        """
        if not pos or any(crew.pos == pos for crew in self.crews.values()):
            pos = (np.random.randint(0,self.grid_size),np.random.randint(0,self.grid_size))
            while any(crew.pos == pos for crew in self.crews.values()):
                pos = (np.random.randint(0,self.grid_size),np.random.randint(0,self.grid_size))
        id = next(self.id_gen)
        new_crew = Type_Chimp_crew(id, pos, strat=strat, ram = self.ram)
        self.crews[id] = new_crew
        return new_crew
    
    def remove_chimp_crews(self):
        to_remove = [key for key, crew in self.crews.items() if crew.energy <= 0]
        for key in to_remove:
            crew = self.crews[key]
            if crew.oasis:
                crew.oasis.occupied = False # Free the oasis
            del self.crews[key]

    def add_oasis(self, pos=None):
        """
        Generate a new oasis
        """
        id = next(self.id_gen)
        if not pos or any(oasis.pos == pos for oasis in self.oases.values()):
            pos = (np.random.randint(0,self.grid_size), np.random.randint(0,self.grid_size))
            while any(oasis.pos == pos for oasis in self.oases.values()):
                pos = (np.random.randint(0,self.grid_size), np.random.randint(0,self.grid_size))

        resource = random.randint(int(self.resource) // 2, int(self.resource) * 3 // 2)
        new_oasis = Oasis(id, pos, resource)
        self.oases[id] = new_oasis
        return new_oasis
    
        
    def create_grid(self):
        grid = np.zeros((self.grid_size, self.grid_size), dtype='f')
        
        for oasis in self.oases.values():
            grid[oasis.X, oasis.Y] = 50
        for crew in self.crews.values():
            grid[crew.X, crew.Y] += crew.strat + 1
        self.grid = grid


    def run(self, prob_win = 1/2):
        """
        Run the model for one time-step

        """
        ids = []
        for oasis in self.oases.values():
            if oasis.resource <= 0:
                ids.append(oasis.id)
        for id in ids:
            del self.oases[id]

        tot_res = sum([oasis.resource for oasis in self.oases.values()])
        required_resource = self.resource_constant * self.n_crews
        missing_resource = required_resource - tot_res

        if missing_resource > 0:
            num_oases_to_add = int(np.ceil(missing_resource / self.resource))
            if num_oases_to_add > self.grid_size**2 - (len(self.oases.values()) + len(self.crews.values())):
                num_oases_to_add = self.grid_size**2 - (len(self.oases.values()) + len(self.crews.values()) + 1)

            for _ in range(num_oases_to_add):
                self.add_oasis()

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
                    crew.recent_history.append(0)
                    crew.recent_history = crew.recent_history[1:]


                # Occupied oasis => Play game
                
                elif neighboring_oases[1]:
                    oasis = self.oases[neighboring_oases[1][0]]
                    other_crew = [crew for crew in self.crews.values() if crew.pos == oasis.pos][0]

                    crew.recent_history.append(1) # record that a conflict happened
                    crew.recent_history = crew.recent_history[1:]
                    #other_crew.recent_history.append(1)
                    #other_crew.recent_history = other_crew.recent_history[1:]
                    
                    # c gets a type depending on strat
                    for c in [crew, other_crew]:
                        if c.strat == 0: # anxious type
                            c.type = 0
                        elif c.strat == 1: # show-off type
                            c.type = 1
                        elif c.strat == 4: # flexible type
                            w = sum(c.recent_history)/len(c.recent_history)
                            c.type = random.choices([0,1], weights=[1-w**self.flex, w**self.flex])[0]
                        elif c.strat == 3 and c.last_opp_type != -1: # resentful type
                            c.type = c.last_opp_type
                        else: # random type
                            c.type = random.choice([0,1])

                    # record the last opponents type
                    crew.last_opp_type = other_crew.type
                    other_crew.last_opp_type = crew.type

                    if crew.type == 0 or crew.type < other_crew.type: # crew gets intimidated out by the defending crew
                        crew.unaccessible_oases.add(oasis.id)
                    
                    elif crew.type == other_crew.type: # display are equal => fight

                        if random.random() > prob_win: # crew losess
                            crew.unaccessible_oases.add(oasis.id) 

                        else: # crew wins
                            other_crew.oasis = None
                            other_crew.pos = crew.pos[:]
                            other_crew.unaccessible_oases.add(oasis.id) 
                            crew.pos = oasis.pos
                            crew.oasis = oasis

                        crew.energy -= self.cost_fight
                        other_crew.energy -= self.cost_fight
                        
                    else:
                        other_crew.oasis = None
                        other_crew.pos = crew.pos[:]
                        other_crew.unaccessible_oases.add(oasis.id)
                        crew.pos = oasis.pos
                        crew.oasis = oasis

                # No oasis near, move closer to oasis
                else:
                    crew.move(self.grid_size, self.oases.values(), self.crews.values())

            else:
                crew.consume()

            
        self.remove_chimp_crews()

        self.create_grid()
        self.data_track[0].append(list(self.crews.values()))
        self.data_track[1].append(list(self.oases.values()))

        # seasonal effect : between the 500th and 800th steps there are bigger/rarer oases
        if self.seasons:
            if len(self.data_track[0]) in [500, 1100, 1700]:
                self.resource *= 2
            
            if len(self.data_track[0]) == [800, 1400]:
                self.resource //= 2