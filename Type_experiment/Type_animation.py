from Type_model import Type_Model as Model
import matplotlib.pyplot as plt
from matplotlib import animation

sim_length = 300
n_types = 3
model = Model(10*n_types, 35, n_types, 20)
fig, ax = plt.subplots()
img = ax.imshow(model.grid, vmin=-1, vmax=n_types)

def update_ani(frame):
    model.run()
    img.set_data(model.grid)
    ax.set_title(f"Time Step: {frame}")
    return [img]

ani = animation.FuncAnimation(fig, update_ani, frames=sim_length, interval=1, blit=False)
ani.save("chimp_simulation.mp4", fps=10)