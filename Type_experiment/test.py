from Type_model import Type_Model as Model
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

# Parameters
n_sim = 100
sim_length = 2000
t = np.linspace(1, sim_length, sim_length)
flex = 2  # Fixed flexibility level
n_types_names = ['Anxious', 'Agressive', 'Random', 'Resentful', 'Flexible']
n_types = len(n_types_names)

# Storage
data_track = []
food_per_chimp_ = []

# Simulations
for _ in tqdm(range(n_sim)):
    food_per_chimp = []
    model = Model(
        10 * n_types, 100, n_types, 20,
        resource_per_oasis=150, cost_fight=30,
        flexible=flex, seasons=True
    )

    for _ in range(sim_length):
        model.run()
        if model.crews:
            food = sum(o.resource for o in model.oases.values())
            pop = sum(c.crew_size for c in model.crews.values())
            food_per_chimp.append(food / (100 * pop) if pop > 0 else 0)
        else:
            food_per_chimp.append(0)

    data_track.append(model.data_track[0])
    food_per_chimp_.append(food_per_chimp)

# Plot
fig, ax = plt.subplots(figsize=(14, 8))

for i in range(n_types):
    n_types_i = np.array([
        [len([crew for crew in step if crew.strat == i]) for step in sim]
        for sim in data_track
    ])
    mean_type = np.mean(n_types_i, axis=0)
    ax.plot(t, mean_type, label=n_types_names[i])

# Add seasonal markers
for start in [500, 1100, 1700]:
    ax.axvspan(start, start + 300, color='gray', alpha=0.05)
    ax.axvline(start, color='black', linestyle='--')
    ax.axvline(start + 300, color='black', linestyle='--')

# Decorate plot
final_pop = sum(np.mean([
    [len([crew for crew in step if crew.strat == i]) for step in sim]
    for sim in data_track
], axis=0)[-1] for i in range(n_types))

ax.set_title(f'cost of fight = {30}, final pop = {final_pop:.2f}', fontsize=16)
ax.set_xlabel('Time')
ax.set_ylabel('Number of Agents')
ax.legend(loc='upper right')
plt.tight_layout()
plt.savefig("Type_experiment/type_crews_over_time_flex_fixed.png", dpi=300)
plt.show()
