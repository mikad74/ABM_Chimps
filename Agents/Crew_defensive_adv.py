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

    def conflict(self, other_crew, oasis, cF=20, cL=10, cI=5, cR=0):
        """
        two-stage game with distinct attacker/defender pay-offs.
        cL plays the role of cd (search cost); cF is cf (fight cost).
        """

        # -------- identify roles --------
        self_is_attacker = (other_crew.oasis is oasis)
        R = oasis.resource
        t_self  = getattr(self,  'type', 1) or 1   # 0 / 1 / 2
        t_other = getattr(other_crew, 'type', 1) or 1

        # -------- display outcome probabilities --------
        # attacker perspective:   pd > pt > pi when stronger → defender sees the opposite
        def probs(t_att, t_def):
            if t_att > t_def:   return 1.0, 0.0, 0.0   # dominate
            if t_att < t_def:   return 0.0, 1.0, 0.0   # intimidated
            return 0.0, 0.0, 1.0                       # tie, leads to fight
        pd, pi, pt = probs(t_self, t_other) if self_is_attacker else probs(t_other, t_self)

        # -------- fight win chance --------
        s_self  = self.crew_size  * self.energy
        s_other = other_crew.crew_size * other_crew.energy
        pw      = 0.5 if s_self + s_other == 0 else s_self / (s_self + s_other)

        # -------- sample display outcome --------
        r = random.random()
        if r < pd:                          # display domination
            if self_is_attacker:
                self._claim_oasis(oasis, other_crew)
                self.energy       += R
                other_crew.energy -= R + cL
            else:                           # defender dominates
                other_crew.energy += R      # keeps resource
                self.energy       -= cL
            return

        if r < pd + pi:                     # intimidated by display
            if self_is_attacker:
                self.energy -= cL           # pays search cost
            # defender gains nothing, already has oasis
            return

        # -------- tie leads to fight --------
        self.energy       -= cF
        other_crew.energy -= cF
        self_wins = random.random() < pw

        if self_wins:
            if self_is_attacker:
                self._claim_oasis(oasis, other_crew)
                self.energy       += R
                other_crew.energy -= R + cL
            else:                           # defender wins fight
                other_crew._claim_oasis(oasis, self)  # attacker pushed away
                self.energy -= cL
        else:
            # self loses fight
            if self_is_attacker:
                self.energy -= cL
            else:
                self.energy       -= R + cL
                other_crew.energy += R       # attacker takes oasis
                other_crew._claim_oasis(oasis, self)



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