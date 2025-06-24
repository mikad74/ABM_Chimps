from Type_model import Type_Model as Model
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np

sim_length = 500
t = np.linspace(1, sim_length, sim_length)
cost_fight_values = [10, 20, 50, 100]
n_types_names = ['Anxious', 'Show-off', 'Random', 'Resentful']
n_types = len(n_types_names)
model = Model(5 * n_types, 100, n_types, 20, cost_fight=10)
fig, ax = plt.subplots()
img = ax.imshow(model.grid, vmin=0, vmax=2)

def update_ani(frame):
    model.run()
    img.set_data(model.grid)
    ax.set_title(f"Time Step: {frame}")
    return [img]

ani = animation.FuncAnimation(fig, update_ani, frames=sim_length, interval=1, blit=False)
ani.save("chimp_simulation.mp4", fps=10)