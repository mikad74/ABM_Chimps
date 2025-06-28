import numpy as np
import matplotlib.pyplot as plt
import json
from SALib.sample import saltelli
from SALib.analyze import sobol
from tqdm import tqdm
from Type_model import Type_Model as Model

# Define problem
problem = {
    'num_vars': 3,
    'names': ['cost of fight', 'avg food per oasis', 'total food in domain'],
    'bounds': [
        [10, 100],
        [50, 200],
        [80, 300],
    ]
}

# Sample parameters
param_values = saltelli.sample(problem, 1024)

# Output names
output_names = ['Total Pop', 'Anxious Pop', 'Resentful Pop', 'Random Pop', 'Flexible Pop', 'Show-off Pop']

# Run model
def run_model(params):
    p1, p2, p3 = params
    model = Model(50, 100, 5, 20, cost_fight=p1, resource_per_oasis=p2, resource_constant=p3)
    sim_length = 2000
    for _ in range(sim_length):
        model.run()

    final_step = model.data_track[0][-1]
    total_pop = sum([crew.crew_size for crew in final_step])
    type_counts = [0] * 5
    for crew in final_step:
        if 0 <= crew.strat < 5:
            type_counts[crew.strat] += crew.crew_size
    return [total_pop] + type_counts

# Run simulations
results = np.array([run_model(params) for params in tqdm(param_values)])
np.save("results.npy", results)

# Analyze and plot
sensitivity_data = {}
n_outputs = len(output_names)
cols = 3
rows = int(np.ceil(n_outputs / cols))
fig, axs = plt.subplots(rows, cols, figsize=(cols * 6, rows * 5))
axs = axs.flatten()

for i, name in enumerate(output_names):
    Si = sobol.analyze(problem, results[:, i])
    sensitivity_data[name] = {k: Si[k].tolist() for k in Si}

    # Individual plot
    fig_ind, ax_ind = plt.subplots(figsize=(8, 5))
    bar_width = 0.35
    x = np.arange(len(problem['names']))

    s1 = Si['S1']
    st = Si['ST']
    s1_conf = Si['S1_conf']
    st_conf = Si['ST_conf']

    ax_ind.bar(x - bar_width/2, s1, width=bar_width, yerr=s1_conf, label='First-order', color='blue')
    ax_ind.bar(x + bar_width/2, st, width=bar_width, yerr=st_conf, label='Total-order', color='gold')
    ax_ind.set_xticks(x)
    ax_ind.set_xticklabels(problem['names'])
    ax_ind.set_ylabel('Sensitivity Index')
    ax_ind.set_title(f"Sensitivity - {name}")
    ax_ind.legend()
    plt.tight_layout()
    plt.savefig(f"Type_experiment/sensitivity_{name.replace(' ', '_')}.png", dpi=300)
    plt.close()

    # Plot in combined grid
    axs[i].bar(x - bar_width/2, s1, width=bar_width, label='S1', color='blue')
    axs[i].bar(x + bar_width/2, st, width=bar_width, label='ST', color='orange')
    axs[i].set_xticks(x)
    axs[i].set_xticklabels(problem['names'])
    axs[i].set_title(name)
    axs[i].set_ylim(0, 1)

# Clean up empty subplots
for j in range(i + 1, len(axs)):
    fig.delaxes(axs[j])

# Save combined grid
handles, labels = axs[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper right', ncol=2)
plt.suptitle("Sobol Sensitivity Indices Across Outputs", fontsize=16, y=1.02)
plt.tight_layout()
plt.savefig("Type_experiment/sensitivity_combined_grid.png", dpi=300, bbox_inches='tight')
plt.close()
