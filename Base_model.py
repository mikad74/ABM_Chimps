from Model.Model import Model as Model
import random

class TestingModel(Model):
    def __init__(self, n_crews, n_oases, grid_size, oasis_spawn_chance=.05):
        super().__init__(n_crews, n_oases, grid_size, oasis_spawn_chance)


    def run(self):
        """
        Run the model for one time-step

        """


        # Remove oasis if empty TODO: Spawn new oases
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
                    crew.unaccessible_oases.add(neighboring_oases[1][0]) # TODO: Play game
                
                # No oasis near, move closer to oasis
                else:
                    crew.move(self.grid_size, self.oases.values(), self.crews.values())
            else:
                crew.consume()

        self.create_grid()
        self.data_track[0].append(self.crews.values())
        self.data_track[1].append(self.oases.values())
