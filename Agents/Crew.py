from .Base import Agent
import random

def euclidean_distance(pos1, pos2):
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

class Chimp_crew(Agent):
    def __init__(self, id, pos, crew_size=10, initial_energy=100, type=None):
        self.crew_size = crew_size # size of crew
        self.id = id
        self.pos = pos # position of the crew on the spatial domain
        self.energy = initial_energy # energy of our crew: goes up when the crew is currently occupying a resource rich oasis, goes down whem the crew moves, fights
        self.oasis = None
        self.unaccessible_oases = set()
        self.type = type 

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

        
        
        if len(available_nbh)>1 and oases:
            # based on global knowledge of all oases, we pick the closest
            accessible_oases = [oasis for oasis in oases if oasis.id not in self.unaccessible_oases]
            if accessible_oases:
                closest_oasis = min(accessible_oases, key=lambda oasis: euclidean_distance(oasis.pos, self.pos))

                distances2oasis = [euclidean_distance(closest_oasis.pos, pos) for pos in available_nbh]
                
                # the least the distance the higher the chance to be picked as next pos
                weights_ = [(1-(dist / sum(distances2oasis)))**motion_accuracy for dist in distances2oasis]
                
                weights = [w/sum(weights_) for w in weights_]

                # we pick new position randomly from the possible ones, with a probability weight depending on "weights"
                self.pos = random.choices(available_nbh, weights=weights)[0]

            else:
                self.pos = random.choices(available_nbh)[0]


        elif len(available_nbh) == 1:
            self.pos = available_nbh[0]
    
    def consume(self): # TODO: expand consume
        food, remaining = self.oasis.get_consumed(self.crew_size * 3)
        self.energy += food
        if remaining <= 0 :
            self.oasis = None
        # depending on size, the crew gains energy while oasis loses ressource

if __name__ == "__main__":
    pass