from Type_model import Type_Model as Model
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np

sim_length = 2000
t = np.linspace(1, sim_length, sim_length)
n_types_names = ['Anxious', 'Show-off', 'Random', 'Flexible', 'Resentful']
n_types = len(n_types_names)
model = Model(10 * n_types, 100, n_types, 20, resource = 150, cost_fight = 10)
fig, ax = plt.subplots()
img = ax.imshow(model.grid, vmin=0, vmax=3)

def update_ani(frame):
    model.run()
    n_crew = len(model.data_track[0][-1])
    food = sum([oasis.resource for oasis in model.data_track[1][-1]])
    if n_crew > 0:
        food_crew = food/n_crew
    else:
        food_crew = 'no crews'
    img.set_data(model.grid)
    ax.set_title(f"Number of crews: {n_crew}, food per crew = {food_crew}, type step = {frame}")
    return [img]

ani = animation.FuncAnimation(fig, update_ani, frames=sim_length, interval=1, blit=False)
ani.save("Type_experiment/chimp_simulation.mp4", fps=20)