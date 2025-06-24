from .Base import Agent
import random

def euclidean_distance(pos1, pos2):
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

class Chimp_crew(Agent):
    def __init__(self, id, pos, crew_size=10, initial_energy=100, consumption_rate=1, expenditure=1):
        self.crew_size = crew_size # size of crew
        self.id = id
        self.pos = pos # position of the crew on the spatial domain
        self.energy = initial_energy # energy of our crew: goes up when the crew is currently occupying a resource rich oasis, goes down whem the crew moves, fights
        self.oasis = None
        self.crew_consumption_rate = consumption_rate
        self.crew_energy_expenditure = expenditure
        self.unaccessible_oases = set()

    #************THE CONFLICT METHOD IS NOT BEING USED IN THE TYPE-INTERPRETATION*************
    #there, the conflict is implemented within the model
    
    
    
    def conflict(self, other_crew, oasis, 
                 cF=20, #should be based on their size
                 cL=10, #should be  based on the size of the oasis
                 cI=5, 
                 cR=0):
        '''
        this function implements the valuation that a crew assigns to a ressource (benefit) depending on how
        hard it might be to take it over (cost)
        '''
        # ---------- shorthand variables ----------
        V = oasis.resource                       # reward if you end up owning the oasis
        s_self   = self.crew_size
        s_other  = other_crew.crew_size
        if s_self + s_other == 0:                # avoid 0-division
            p = 0.5
        else:
            p = s_self / (s_self + s_other)      # win prob if a fight happens

        q = max(0.0, min(0.9, 0.2 + 0.6 * (p - 0.5)))   # back-down chance after display

        # ---------- expected utilities ----------
        U_fight      = p * (V - cF) + (1 - p) * (-cF - cL)
        U_intimidate = -cI + q * V + (1 - q) * U_fight
        U_retreat    = -cR

        # ---------- choose action ----------
        if U_intimidate >= max(U_fight, U_retreat):
            action = "intimidate"
        elif U_fight >= U_retreat:
            action = "fight"
        else:
            action = "retreat"

        # ---------- enact consequences ----------
        if action == "retreat":
            self.energy += U_retreat             # just subtracts cR (0 by default)
            self.unaccessible_oases.add(oasis.id)
            #return action #do we need to return it?

        # pay display cost first
        self.energy -= cI

        # Does opponent yield to the display?
        if action == "intimidate" and random.random() < q:
            self._claim_oasis(oasis, other_crew)
            #return action # maybe we need this at some point
            
        else: 
            action = "fight" #right? 
            
        # ************"fight" NOT USED, USE IT************
            

        # ---------- fight (either chosen directly or after failed display) ----------
        self.energy        -= cF
        other_crew.energy  -= cF
        self_wins = random.random() < p
        if self_wins:
            other_crew.energy -= cL
            self._claim_oasis(oasis, other_crew)
        else:
            self.energy -= cL
            other_crew._claim_oasis(oasis, self)
        #return "fight" # maybe we need this at some point

    def _claim_oasis(self, oasis, loser):
        """Helper: self takes oasis; loser becomes nomad and marks it inaccessible."""
        self.pos     = oasis.pos
        self.oasis   = oasis
        oasis.occupied = True

        loser.oasis  = None
        loser.unaccessible_oases.add(oasis.id)



    def move(self, grid_length, oases, crews, motion_accuracy = 100):
        neighbourhood = [[self.X + di, self.Y + dj] for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, 1), (1, -1)] if 0 <= self.X + di < grid_length and 0 <= self.Y + dj < grid_length]
        # here check for neighboring crews to avoid collision
        available_nbh = [pos for pos in neighbourhood if pos not in[crew.pos for crew in crews]]

        
        
        self.energy -= self.crew_size * self.crew_energy_expenditure
        if len(available_nbh) > 1 and oases:
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
        food, remaining = self.oasis.get_consumed(self.crew_size * self.crew_consumption_rate)
        self.energy += food
        if remaining <= 0 :
            self.oasis = None
        # depending on size, the crew gains energy while oasis loses resource

if __name__ == "__main__":
    pass