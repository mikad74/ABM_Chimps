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
    def __init__(self, id, pos, crew_size=10, initial_energy=100, strat=None):
        super().__init__(id, pos, crew_size, initial_energy)
        self.strat = strat
        self.type = None
        self.last_opp_type = -1

    def intimidate(self, other_crew, prob_win, oasis, cost_bluff=0):
        won = 0
        if random.random() > prob_win: # crew loses
            self.unaccessible_oases.add(oasis) 

        else: # crew wins
            other_crew.oasis = None
            other_crew.pos = self.pos[:]
            other_crew.unaccessible_oases.add(oasis) 
            self.pos = oasis.pos
            self.oasis = oasis
            won = 'won'
        
        # pay cost of bluffing in any event
        self.energy -= cost_bluff
        other_crew.energy -= cost_bluff
        
        return won
            
    def fight(self, other_crew, prob_win, oasis, cost_fight, constant_win=True):
        # define if the crew wins or loses
        lose = False
        if constant_win:
            if random.random() > prob_win: # when prob_win is constant - define winning prob solely by it
                lose = True           
        else: # condition wins on the differences between the crews
            prob_win = self.energy / (self.energy + other_crew.energy + 0.00001) #to prevent division by zero
            #if they are both at <= 0, they will be removed after this step anyways
            if random.random() > prob_win: 
                lose = True

        # assign consequences
        if lose:
            self.unaccessible_oases.add(oasis)        
        else: # crew wins
            other_crew.oasis = None
            other_crew.pos = self.pos[:]
            other_crew.unaccessible_oases.add(oasis) 
            self.pos = oasis.pos
            self.oasis = oasis

        # pay cost of fight in any event
        self.energy -= cost_fight
        other_crew.energy -= cost_fight

    def reclaim(self, other_crew, oasis):
        other_crew.oasis = None
        other_crew.pos = self.pos[:]
        other_crew.unaccessible_oases.add(oasis) 
        self.pos = oasis.pos
        self.oasis = oasis

class Type_Model:
    def __init__(self, n_crews, n_oases, n_types, grid_size, cost_fight = 10, oasis_spawn_chance=.05):
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
        new_crew = Type_Chimp_crew(id, pos, strat=strat)
        self.crews[id] = new_crew
        return new_crew
    
    def remove_chimp_crews(self):
        to_remove = [key for key, crew in self.crews.items() if crew.energy <= 0]
        for key in to_remove:
            crew = self.crews[key]
            if crew.oasis:
                crew.oasis.occupied = False  # Free the oasis
            del self.crews[key]


    def add_oasis(self, pos=None):
        """
        Generate a new oasis
        """
        id = next(self.id_gen)
        if not pos or any(oasis.pos == pos for oasis in self.oases.values()):
            pos = (np.random.randint(0,self.grid_size),np.random.randint(0,self.grid_size))
            while any(oasis.pos == pos for oasis in self.oases.values()):
                pos = (np.random.randint(0,self.grid_size),np.random.randint(0,self.grid_size))
        resource = random.randint(250, 280)
        new_oasis = Oasis(id, pos, resource)
        self.oases[id] = new_oasis
        return new_oasis
    
        
    def create_grid(self):
        grid = np.zeros((self.grid_size, self.grid_size), dtype='f')
        
        for oasis in self.oases.values():
            grid[oasis.X, oasis.Y] = -1
        for crew in self.crews.values():
            grid[crew.X, crew.Y] =+ 1 + crew.strat
        self.grid = grid


    def run(self, 
            prob_win = 1/2, # default stable random prob of winning a fight or a bluff-fight
            agressive = False, # default for not having type "agressive", adds sophisticated version of "agressive" if True
            constant_win=True, # default for constant prob_win that is independent of size, makes fight dependent on size if False
            cost_bluff = 0 # default is no cost, but you can pass it to see if the dynamics changes
            ):
        """
        Run the model for one time-step

        """

        ids = []
        for oasis in self.oases.values():
            if oasis.resource <= 0:
                ids.append(oasis.id)
        for id in ids:
            del self.oases[id]

        n_chimps = sum([crew.crew_size for crew in self.crews.values()])
        tot_res = sum([oasis.resource for oasis in self.oases.values()])

        if tot_res < 80 * n_chimps :
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

                # Occupied oasis => Play game
                elif neighboring_oases[1]:
                    
                    oasis = self.oases[neighboring_oases[1][0]]
                    other_crew = [crew for crew in self.crews.values() if crew.pos == oasis.pos][0]
                    # other_crew is by default defender: they are always already on the oasis
                    
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
                        elif c.strat == 4: # agressive type
                            c.type = 2
                    
                    # record the last opponents type
                    crew.last_opp_type = other_crew.type
                    other_crew.last_opp_type = crew.type
                    
                    
                    #------------record the payoff------------
                    
                    #____________DEFINED BY ARGUMENT agressive ____________
                    '''
                    Also accommodates the dependency of winning on the crew energy
                    by adding an optional constant_win argument into the .fight method
                    '''
                    if agressive:
                                                
                        if crew.type == 0: #if anxious
                            crew.unaccessible_oases.add(oasis) #retreat
                        
                        elif other_crew.type == 0: #if the other one is anxious
                            crew.reclaim(other_crew, oasis) #always get their oasis
                            
                        elif crew.type == 1: #if show-off
                            result = crew.intimidate(other_crew, prob_win, oasis, cost_bluff = cost_bluff) # prob 1/2 to win, but no/lower cost 
                        
                            #if the other one is no fighter, it just ends here, whatever the result was
                            #if the defender is a fighter, and they lost bluffing, then there is a fight    
                            if other_crew.type == 2 and result: #the crew won -> the other_crew lost
                                crew.fight(other_crew, prob_win, oasis, self.cost_fight, constant_win=constant_win)
                        
                        elif crew.type == 2:
                            crew.fight(other_crew, prob_win, oasis, self.cost_fight, constant_win=constant_win) #nothing depends on the defender, the crew just attacks
                                    
                    #*******ORIGINAL VERSION BY BALTHAZAR, practically only type 0 and type 1*********

                    #Also accommodates primitive agressive type, corresponding to visualisation "with_agressive"
                    #type 0 + type 1 corresponds to "without_agressive"

                    else:
                        if crew.type == 0 or crew.type < other_crew.type: # crew gets intimidated out by the defending crew
                            crew.unaccessible_oases.add(oasis)                 
            
                        elif crew.type == other_crew.type: # fight when same type
                            crew.fight(other_crew, prob_win, oasis, self.cost_fight)
                        
                        elif crew.type == 4 or other_crew.type == 4: 
                            # one of them is agressive and none is anxious
                            crew.fight(other_crew, prob_win, oasis, self.cost_fight)
                            
                        else: # crew.type > other_crew.type
                            crew.reclaim(other_crew, oasis)

                    #------------payoff recorded---------------
                    
                # No oasis near, move closer to oasis
                else:
                    crew.move(self.grid_size, self.oases.values(), self.crews.values())
            else:
                crew.consume()

        for crew in self.crews.values():
            crew.energy -= crew.crew_size
            
        self.remove_chimp_crews()

        self.create_grid()
        self.data_track[0].append(list(self.crews.values()))
        self.data_track[1].append(list(self.oases.values()))