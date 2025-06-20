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
from Model.Model import Model

class Type_Chimp_crew(Chimp_crew):
    def __init__(self, id, pos, crew_size=10, initial_energy=100, strat=None, consumption_rate=1, expenditure=1):
        super().__init__(id, pos, crew_size, initial_energy)
        self.strat = strat
        self.type = None
        self.last_opp_type = -1


class Type_Model(Model):
    def __init__(self, n_crews, grid_size, n_types,  cost_fight = 10, oasis_spawn_proportional=True, abundance_factor=10, oasis_density=0.3, food_consumption_speed=nk1.5):
        '''
        n_crews (int): number of initial chimp crews
        n_oases (int): number of initial oases
        grid_size(int): length of the edge of the square grid
        '''
        super().__init__(n_crews, grid_size, initialise_crews=False, oasis_spawn_proportional=oasis_spawn_proportional, abundance_factor=abundance_factor, oasis_density=oasis_density, food_consumption_speed=food_consumption_speed)
        self.crews = {}
        self.initial_n_chimps = self.initialize_typed_crews(n_crews, n_types)
        self.avg_oasis_size = self.food_required / (oasis_density * grid_size * grid_size )
        self.update_oases()
        self.cost_fight = cost_fight
        self.create_typed_grid()
        pass

    def initialize_typed_crews(self, n_crews, n_types):
        for i in range(n_crews):
            self.add_chimp_crew(strat=i%n_types)
        return self.n_chimps

    def add_chimp_crew(self, pos=None, strat=None):
        """
        Generate a crew of chimps as an agent
        """
        if not pos or any(crew.pos == pos for crew in self.crews.values()):
            pos = (np.random.randint(0,self.grid_size),np.random.randint(0,self.grid_size))
            while any(crew.pos == pos for crew in self.crews.values()):
                pos = (np.random.randint(0,self.grid_size),np.random.randint(0,self.grid_size))
        id = next(self.id_gen)
        new_crew = Type_Chimp_crew(id, pos, strat=strat, consumption_rate=self.crew_consumption_rate)
        self.crews[id] = new_crew
        return new_crew
    


    def remove_chimp_crews(self):
        to_remove = [key for key, crew in self.crews.items() if crew.energy <= 0]
        for key in to_remove:
            crew = self.crews[key]
            if crew.oasis:
                crew.oasis.occupied = False  # Free the oasis
            del self.crews[key]

        
    def create_typed_grid(self):
        grid = np.zeros((self.grid_size, self.grid_size), dtype='f')
        
        for oasis in self.oases.values():
            grid[oasis.X, oasis.Y] = -1
        for crew in self.crews.values():
            grid[crew.X, crew.Y] =+ 1 + crew.strat
        self.grid = grid


    def run(self, prob_win = 1/2):
        """
        Run the model for one time-step

        """

        self.update_oases()

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
                    other_crew = [crew for crew in self.crews.values() if crew.pos == oasis.pos][0]
                    
                    # c gets a type depending on strat
                    for c in [crew, other_crew]:
                        if c.strat == 0: # anxious type
                            c.type = 0
                        elif c.strat == 1: # show-off type
                            c.type = 1
                        elif c.strat == 2: # random type
                            c.type = random.choice([0,1])
                        elif c.strat == 3: # resentful type
                            if c.last_opp_type == -1:
                                c.type = random.choice([0,1])
                            else:
                                c.type = c.last_opp_type
                    
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


        # for crew in self.crews.values():
        #     crew.energy -= crew.crew_size
            
        self.remove_chimp_crews()

        self.create_grid()
        self.data_track[0].append(list(self.crews.values()))
        self.data_track[1].append(list(self.oases.values()))