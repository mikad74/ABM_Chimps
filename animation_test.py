from Base_model import *
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.markers import MarkerStyle
from matplotlib import animation
from matplotlib.colors import LinearSegmentedColormap

# Define a Pac-Man shape (wedge from a circle)
theta = np.linspace(0.25 * np.pi, 1.75 * np.pi, 30)  # open mouth
verts = [(0, 0)] + [(np.cos(t), np.sin(t)) for t in theta] + [(0, 0)]
codes = [Path.MOVETO] + [Path.LINETO] * (len(verts) - 2) + [Path.CLOSEPOLY]

pacman_path = Path(verts, codes)
pacman_marker = MarkerStyle(pacman_path)

# Define a dark purple gradient colormap (from black to dark purple to lighter purple)
dark_purple_cmap = LinearSegmentedColormap.from_list(
    'dark_purple', ["#29044e", "#29044e","#29044e","#29044e"], N=256
)

n_sim = 500
model = Model(5, 20, 20)

fig, ax = plt.subplots()
img = ax.imshow(model.grid, cmap=dark_purple_cmap)

# Scatter plots for each value
scatter_2 = ax.scatter([], [], marker='d', c='white', s=100)  # hexagon
scatter_1 = ax.scatter([], [], marker=pacman_marker, c='yellow', s=100)    # diamond
scatter_3 = ax.scatter([], [], marker='o', c='yellow', s=150)   # star

def update_ani(frame):
    model.run()
    grid = model.grid
    img.set_array(grid)
    ax.set_title(f"Time Step: {frame}")

    # Separate coordinates by value
    xs_1, ys_1 = [], []
    xs_2, ys_2 = [], []
    xs_3, ys_3 = [], []

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            val = grid[i, j]
            if val == 1:
                xs_1.append(j)
                ys_1.append(i)
            elif val == 2:
                xs_2.append(j)
                ys_2.append(i)
            elif val == 3:
                xs_3.append(j)
                ys_3.append(i)
# Update scatter data
    scatter_1.set_offsets(np.array(list(zip(xs_1, ys_1))) if xs_1 else np.empty((0, 2)))
    scatter_2.set_offsets(np.array(list(zip(xs_2, ys_2))) if xs_2 else np.empty((0, 2)))
    scatter_3.set_offsets(np.array(list(zip(xs_3, ys_3))) if xs_3 else np.empty((0, 2)))

    return [img, scatter_1, scatter_2, scatter_3]

ani = animation.FuncAnimation(fig, update_ani, frames=n_sim, interval=100, blit=False)
ani.save("chimp_simulation.mp4", fps=10)