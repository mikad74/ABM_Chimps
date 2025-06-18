from Base_model import *
import matplotlib.pyplot as plt
from matplotlib import animation

n_sim = 100
model = Model(20, 20, 50)
# model.add_oasis((2,2))
# model.add_chimp_crew((0,1))
# model.add_chimp_crew((1,0))
# model.add_chimp_crew((1,2))
# model.add_chimp_crew((2,1))
# model.grid = model.create_grid()
fig, ax = plt.subplots()
img = ax.imshow(model.grid)

def update_ani(frame):
    model.run()
    img.set_array(model.grid)
    ax.set_title(f"Time Step: {frame}")
    return [img]

ani = animation.FuncAnimation(fig, update_ani, frames=n_sim, interval=1, blit=False)
ani.save("chimp_simulation.mp4", fps=10)

for oasis in model.oases.values():
    print(vars(oasis))
for crew in model.crews.values():
    print(vars(crew))