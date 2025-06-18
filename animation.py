from Base_model import *
import matplotlib.pyplot as plt
from matplotlib import animation

n_sim = 500
model = Model(5, 30, 30)
fig, ax = plt.subplots()
img = ax.imshow(model.grid)

def update_ani(frame):
    model.run()
    img.set_array(model.grid)
    ax.set_title(f"Time Step: {frame}")
    # for oasis in model.oases.values():
    #     print(vars(oasis))
    # for crew in model.crews.values():
    #     print(vars(crew))
    return [img]

ani = animation.FuncAnimation(fig, update_ani, frames=n_sim, interval=1, blit=False)
ani.save("chimp_simulation.mp4", fps=10)

for oasis in model.oases.values():
    print(vars(oasis))
for crew in model.crews.values():
    print(vars(crew))