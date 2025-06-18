from Base_model import *
import matplotlib.pyplot as plt
from matplotlib import animation

n_sim = 100
model = Model(5, 20, 20)
fig, ax = plt.subplots()
img = ax.imshow(model.grid, vmin=0, vmax=3)

def update_ani(frame):
    model.run()
    img.set_data(model.grid)
    ax.set_title(f"Time Step: {frame}")
    return [img]

ani = animation.FuncAnimation(fig, update_ani, frames=n_sim, interval=1, blit=False)
ani.save("chimp_simulation.mp4", fps=10)
