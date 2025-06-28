from Type_experiment.Type_model  import Type_Model as Model
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.markers import MarkerStyle
from matplotlib import animation
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

# Define a Pac-Man shape (wedge from a circle)
theta = np.linspace(0.25 * np.pi, 1.75 * np.pi, 30)  # open mouth
verts = [(0, 0)] + [(np.cos(t), np.sin(t)) for t in theta] + [(0, 0)]
codes = [Path.MOVETO] + [Path.LINETO] * (len(verts) - 2) + [Path.CLOSEPOLY]

pacman_path = Path(verts, codes)
pacman_marker = MarkerStyle(pacman_path)

# Define a dark purple gradient colormap (from black to dark purple to lighter purple)
dark_purple_cmap = LinearSegmentedColormap.from_list(
    'dark_purple', ["#18044e","#18044e","#18044e","#18044e"], N=256
)

sim_length = 2000
model = Model(50, 100, 5, 20, cost_fight=10, resource=100)

fig, ax = plt.subplots(figsize=(8,8))
img = ax.imshow(model.grid, cmap=dark_purple_cmap)

# Scatter plots for each value
scatter_2 = ax.scatter([], [], marker='*', c='white', s=100)  # hexagon
scatter_10 = ax.scatter([], [], marker=pacman_marker, c='yellow', s=150)    # diamond
scatter_11 = ax.scatter([], [], marker=pacman_marker, c='orange', s=150)    # diamond
scatter_12 = ax.scatter([], [], marker=pacman_marker, c='green', s=150)    # diamond
scatter_13 = ax.scatter([], [], marker=pacman_marker, c='red', s=150)    # diamond
scatter_14 = ax.scatter([], [], marker=pacman_marker, c='purple', s=150)    # diamond
scatter_30 = ax.scatter([], [], marker='o', c='yellow', s=150)   # star
scatter_31 = ax.scatter([], [], marker='o', c='orange', s=150)   # star
scatter_32 = ax.scatter([], [], marker='o', c='green', s=150)   # star
scatter_33 = ax.scatter([], [], marker='o', c='red', s=150)   # star
scatter_34 = ax.scatter([], [], marker='o', c='purple', s=150)   # star

def update_ani(frame):
    model.run()
    grid = model.grid
    avg_ram = np.mean([sum(crew.recent_history) for crew in model.data_track[0][-1]])
    img.set_array(grid)
    ax.set_title(f"Time Step: {frame}, ram = {avg_ram}")

    # Separate coordinates by value
    xs_10, ys_10 = [], []
    xs_11, ys_11 = [], []
    xs_12, ys_12 = [], []
    xs_13, ys_13 = [], []
    xs_14, ys_14 = [], []
    xs_2, ys_2 = [], []
    xs_30, ys_30 = [], []
    xs_31, ys_31 = [], []
    xs_32, ys_32 = [], []
    xs_33, ys_33 = [], []
    xs_34, ys_34 = [], []

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            val = grid[i, j]
            if val == 1:
                xs_10.append(j)
                ys_10.append(i)
            elif val == 2:
                xs_11.append(j)
                ys_11.append(i)
            elif val == 3:
                xs_12.append(j)
                ys_12.append(i)
            elif val == 4:
                xs_13.append(j)
                ys_13.append(i)            
            elif val == 5:
                xs_13.append(j)
                ys_13.append(i)
            elif val == 50:
                xs_2.append(j)
                ys_2.append(i)
            elif val == 51:
                xs_30.append(j)
                ys_30.append(i)
            elif val == 52:
                xs_31.append(j)
                ys_31.append(i)
            elif val == 53:
                xs_32.append(j)
                ys_32.append(i)
            elif val == 54:
                xs_33.append(j)
                ys_33.append(i)
            elif val == 55:
                xs_34.append(j)
                ys_34.append(i)
# Update scatter data
    scatter_10.set_offsets(np.array(list(zip(xs_10, ys_10))) if xs_10 else np.empty((0, 2)))
    scatter_11.set_offsets(np.array(list(zip(xs_11, ys_11))) if xs_11 else np.empty((0, 2)))
    scatter_12.set_offsets(np.array(list(zip(xs_12, ys_12))) if xs_12 else np.empty((0, 2)))
    scatter_13.set_offsets(np.array(list(zip(xs_13, ys_13))) if xs_13 else np.empty((0, 2)))
    scatter_14.set_offsets(np.array(list(zip(xs_14, ys_14))) if xs_14 else np.empty((0, 2)))

    scatter_2.set_offsets(np.array(list(zip(xs_2, ys_2))) if xs_2 else np.empty((0, 2)))
    scatter_30.set_offsets(np.array(list(zip(xs_30, ys_30))) if xs_30 else np.empty((0, 2)))
    scatter_31.set_offsets(np.array(list(zip(xs_31, ys_31))) if xs_31 else np.empty((0, 2)))
    scatter_32.set_offsets(np.array(list(zip(xs_32, ys_32))) if xs_32 else np.empty((0, 2)))
    scatter_33.set_offsets(np.array(list(zip(xs_33, ys_33))) if xs_33 else np.empty((0, 2)))
    scatter_34.set_offsets(np.array(list(zip(xs_34, ys_34))) if xs_34 else np.empty((0, 2)))


    return [img, scatter_10, scatter_11, scatter_12, scatter_13, scatter_2, scatter_30, scatter_31, scatter_32, scatter_33]

ani = animation.FuncAnimation(fig, update_ani, frames=sim_length, interval=100, blit=False)
ani.save("chimp_simulation.mp4", fps=10, dpi=100)