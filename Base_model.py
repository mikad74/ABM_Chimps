import numpy as np

def euclidean_distance(pos1, pos2):
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

class Model:
    #def __init__(self, grid_length, num_crews, num_oases):
    def __init__(self, n_crews, n_oases, grid_size):
        self.grid_size = grid_size
        self.crews = [self.add_chimp_crew(id) for id  in range(n_crews)]
        self.oases = [self.add_oasis(id) for id in range(n_oases)]
        self.grid = self.create_grid()
        pass

    def add_chimp_crew(self, id):
        pos = (1,2)             #TODO: adjust attributes of crew
        size = 0
        energy = 0
        new_crew = Chimp_crew(id, pos, size, energy)
        return new_crew

    def add_oasis(self, id):
        pos = (0,0)
        size = 0
        new_oasis = Oasis(id, pos, size)
        return new_oasis
    
    def run(self):
        for crew in self.crews:
            X_old, Y_old = crew.pos
            crew.move(self.grid_size, self.grid)
            self.grid[X_old, Y_old] = 0
            if not self.grid[crew.X, crew.Y] == 2:
                self.grid[crew.X, crew.Y] = 1       #TODO: chimp + oasis
            else:
                for oasis in self.oases:
                    print(oasis.pos)
                    if oasis.pos == (crew.X, crew.Y):
                        crew.oasis = oasis
                        print(vars(crew))
                        self.grid[crew.X, crew.Y] = 3

        return 0 
        
    def create_grid(self):
        grid = np.zeros((self.grid_size, self.grid_size))
        for crew in self.crews:
            grid[crew.X, crew.Y] = 1
        for oasis in self.oases:
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
        self.pos = np.array(pos) # position of the crew on the spatial domain
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
        '''
        pre_utility = [[oasis.ressource - cost_fight, oasis.ressource], [- cost_fight - cost_loss, - cost_loss]] # potential outcomes from a conflict
        # look for equilibrium here

        # fight 
        # loss of energy eitherway
        # if win then crew stops being nomad and takes same position as oasis 
        # other crew becomes nomad again and takes an available neighbouring position
        # if loss, crew keeps searching

    def move(self, grid_length, grid): 
        # Random move function for testing
        if self.oasis == None:
            neighbourhood = [[self.X + di, self.Y + dj] for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, 1), (1, -1)] if 0 <= self.X + di < grid_length and 0 <= self.Y + dj < grid_length]
            choice = neighbourhood[np.random.choice(len(neighbourhood))]
            while grid[choice[0], choice[1]] == 1:
                choice = neighbourhood[np.random.choice(len(neighbourhood))]
            self.pos = choice

    def move_(self, grid_length, motion_accuracy = 100):

        i, j = self.pos
        neighbourhood = [[i + di, j + dj] for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, 1), (1, -1)] if 0 <= i + di < grid_length and 0 <= j + dj < grid_length]
        # here check for neighboring crews to avoid collision
        # based on global knowledge of all oases, we pick the closest
        # we select next position depending on how close it is the oasis we selected
        oasis = tt # the selected, closest 

        weights = [1-euclidean_distance(oasis.pos, pos) for pos in neighbourhood]
    
    def consume(self, oasis):
        # depending on size, the crew gains energy while oasis loses ressource
        pass


class Oasis(Agent):
    def __init__(self, id, pos, ressource):
        self.id = id
        self.pos = pos
        self.ressource = ressource
        self.occupied = False
    
    def feed(self, amount):
        food = min(amount, self.resource)
        self.resource -= food
        return food