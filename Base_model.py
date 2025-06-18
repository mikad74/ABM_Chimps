import numpy as np
import random
from itertools import count

def euclidean_distance(pos1, pos2):
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

class Model:
    def __init__(self, n_crews, n_oases, grid_size):
        '''
        n_crews (int): number of initial chimp crews
        n_oases (int): number of initial oases
        grid_size(int): length of the edge of the square grid
        '''
        self.id_gen = count()
        self.grid_size = grid_size
        self.crews = {}
        self.oases = {}
        for _ in range(n_crews):
            self.add_chimp_crew()
        for _ in range(n_oases):
            self.add_oasis()
        self.grid = self.create_grid()
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

    def add_oasis(self, pos=None):
        """
        Generate a new oasis
        """
        id = next(self.id_gen)
        if not pos or any(oasis.pos == pos for oasis in self.oases.values()):
            pos = (np.random.randint(0,self.grid_size),np.random.randint(0,self.grid_size))
            while any(oasis.pos == pos for oasis in self.oases.values()):
                pos = (np.random.randint(0,self.grid_size),np.random.randint(0,self.grid_size))
        size = 1
        new_oasis = Oasis(id, pos, size)
        self.oases[id] = new_oasis
        return new_oasis
    
    def run(self):
        """
        Run the model for one time-step

        """
        ids = []
        for oasis in self.oases.values():
            if oasis.resource <= 0:
                ids.append(oasis.id)
        for id in ids:
            del self.oases[id]
        for crew in self.crews.values():

            # Only move if not feeding at an oasis
            if not crew.oasis:
                X_old, Y_old = crew.pos
                crew.move(self.grid_size, self.oases.values(), self.crews.values())
                self.grid[X_old, Y_old] = 0
                if not self.grid[crew.X, crew.Y] == 2:
                    self.grid[crew.X, crew.Y] = 1       #TODO: chimp + oasis
                

                # When arriving at an oasis attach it to the agent
                else:
                    for oasis in self.oases.values():
                        if oasis.pos == (crew.X, crew.Y) and not oasis.occupied:
                            crew.oasis = oasis
                            oasis.occupied = True
                            self.grid[crew.X, crew.Y] = 3
            
            # If at an oasis, consume
            else:
                crew.consume()
                if crew.oasis == None:
                    self.grid[crew.X, crew.Y] = 1
        
    def create_grid(self):
        grid = np.zeros((self.grid_size, self.grid_size))
        for crew in self.crews.values():
            grid[crew.X, crew.Y] = 1
        for oasis in self.oases.values():
            grid[oasis.X, oasis.Y] = 2
        return grid


        # create chimps crews
        # create oases 
        # track chimps
        # track oases
        # loop for steps(chimps)

        # check for neighboring oases
        # check for oasis status
        # if occupied, try bluff
        # if bluff works you claim the oasis
        # if bluff is insufficient you go on your way and add this oasis to unaccessible_oases 
        # if bluff is a tie (or close enough) fight
        # motion calls for move function

class Agent:
    def __init__(self):
        self.pos = (0,0)
    
    @property
    def X(self):
        return self.pos[0]

    @property
    def Y(self):
        return self.pos[1]


class Chimp_crew(Agent):
    def __init__(self, id, pos, crew_size=10, initial_energy=100):
        self.crew_size = crew_size # size of crew
        self.id = id
        self.pos = pos # position of the crew on the spatial domain
        self.energy = initial_energy # energy of our crew: goes up when the crew is currently occupying a resource rich oasis, goes down whem the crew moves, fights
        self.nomad = True # whether the crew is currently looking for a new source of food
        self.oasis = None
        self.unaccessible_oasis = [] 

    def conflict(self, other_crew, oasis, cost_fight = 20, cost_loss = 10):
        '''
        this function returns the valuation that a crew assigns to a ressource (benefit) depending on how
        hard it might be to take it over (cost)
        '''
        # intimidation round
        
        '''
        V = oasis.resource
        s = crew_size * energy
        cF = cost of fight
        cL = cost of losing the fight
        cI = cost of intimidate
        
        q = prob opponent backs down after the agent intimidates
        q = clip(0.2 + 0.6 * (p - 0.5), 0, 0.9)             0.2 is the threshold
        
        p = prob agent wins the fight
        p = s_self / (s_self + s_other)
        
        U_fight      = p·(V - cF)      + (1 - p)·(-cF - cL)
        U_intimidate = -cI + q·V        + (1 - q)·U_fight
        U_retreat    = 0                                            ?? or -cR?
        
        if U_intimidate ≥ max(U_fight, U_retreat):   INTIMIDATE
        elif U_fight      ≥ U_retreat:               FIGHT
        else:                                        RETREAT

        ______________________________

        I thought we said we only decide intimidate/retreat and a fight happens when both decide to intimidate?

        I think we can model this with what we learned in the lecture about prospect theory since we have the
        case where we need to make a decision that could lead to either a gain or loss from our current energy level.
        We calculate the utility of fighting with the formula  U(x) = π(pi)v(xi) + π(pj)v(xj) from the lecture.
        xi being energy gain from the ressource and xj the loss in energy from fighting and losing.
        I don't know if we really need the parameter cost_loss? I think it's implicit in fighting but not getting the ressource.

        v(xj) includes a positive gain sensitivity parameter and loss aversion parameters. Here we could apply
        the strategy of the chimps -> risk-seeking agents will have a higher valuation for winning and are more likely to bluff.
        The weighting function includes the probility of the outcome i.e. the percieved likelihood of winning the fight.
        We can iteratively modify how p is calculated but I think it needs to include the size of this crew, size of other
        crew and own energy level. Later we could add fight history for smarter chimps.

        The utility for retreating is just 0 and we decide: 
        if U_fight ≥ U_retreat = 0:   INTIMIDATE
        else  RETREAT
        Let me know that you think!

        '''
        pre_utility = [[oasis.ressource - cost_fight, oasis.ressource], [- cost_fight - cost_loss, - cost_loss]] # potential outcomes from a conflict
        # look for equilibrium here

        # fight 
        # loss of energy eitherway
        # if win then crew stops being nomad and takes same position as oasis 
        # other crew becomes nomad again and takes an available neighbouring position
        # if loss, crew keeps searching


    def move(self, grid_length, oases, crews, motion_accuracy = 100):
        neighbourhood = [[self.X + di, self.Y + dj] for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, 1), (1, -1)] if 0 <= self.X + di < grid_length and 0 <= self.Y + dj < grid_length]
        # here check for neighboring crews to avoid collision
        available_nbh = [pos for pos in neighbourhood if pos not in[crew.pos for crew in crews]]

        
        
        if available_nbh and oases:
            # based on global knowledge of all oases, we pick the closest
            closest_oasis = min(oases, key=lambda oasis: euclidean_distance(oasis.pos, self.pos))

            distances2oasis = [euclidean_distance(closest_oasis.pos, pos) for pos in available_nbh]
            
            # the least the distance the higher the chance to be picked as next pos
            weights_ = [(1-(dist / sum(distances2oasis)))**motion_accuracy for dist in distances2oasis]
            weights = [w/sum(weights_) for w in weights_]

            # we pick new position randomly from the possible ones, with a probability weight depending on "weights"
            self.pos = random.choices(available_nbh, weights=weights)[0]

        else:
            self.pos = random.choice(available_nbh)
    
    def consume(self):
        food, remaining = self.oasis.get_consumed(self.crew_size * 3)
        self.energy += food
        if remaining <= 0 :
            self.oasis = None
        # depending on size, the crew gains energy while oasis loses ressource


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