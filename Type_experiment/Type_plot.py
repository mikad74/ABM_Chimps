from Type_model import Type_Model as Model
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

n_sim = 100
sim_length = 3000
t = np.linspace(1, sim_length, sim_length)
cost_fight_values = [20, 50]
resource_values = [25, 50, 75, 100]
n_types_names = ['Anxious', 'Agressive', 'Random', 'Resentful', 'Flexible']
n_types = len(n_types_names)

fig, axs = plt.subplots(1, 2, figsize=(14, 6))
axs = axs.flatten()

for idx, cost_fight in enumerate(tqdm(cost_fight_values)):
    data_track = []
    data_track_oases = []
    food_per_chimp_ = []

    for i in range(n_sim):
        food_per_chimp = []
        model = Model(10 * n_types, 100, n_types, 20, resource_per_oasis = 110, cost_fight = cost_fight, resource_constant=120, seasons=True)
        for j in range(sim_length):
            model.run()
        data_track.append(model.data_track[0])
        data_track_oases.append(model.data_track[1])

    n_types_over_time = []
    for i in range(n_types):
        n_types_i = np.array([[len([crew for crew in step if crew.strat == i]) for step in sim] for sim in data_track])
        
        n_types_over_time.append(np.mean(n_types_i, axis=0))
        axs[idx].plot(t, n_types_over_time[i], label=f"{n_types_names[i]}")
    axs[idx].set_title(f'cost of fight = {cost_fight}, final pop = {sum([n_types_over_time[i][-1] for i in range(n_types)]):.2f}')
    axs[idx].set_xlabel('Time')
    if model.seasons:
        axs[idx].axvline(500, color='black', linestyle='--')
        axs[idx].axvline(800, color='black', linestyle='--')
        axs[idx].axvspan(500, 800, color='gray', alpha=0.05)
        axs[idx].axvline(1100, color='black', linestyle='--')
        axs[idx].axvline(1400, color='black', linestyle='--')
        axs[idx].axvspan(1100, 1400, color='gray', alpha=0.05)
        axs[idx].axvline(1700, color='black', linestyle='--')
        axs[idx].axvline(2000, color='black', linestyle='--')
        axs[idx].axvspan(1700, 2000, color='gray', alpha=0.05)
    axs[idx].set_ylabel('Number of Agents')
    axs[idx].legend()

plt.tight_layout()
plt.savefig("Type_experiment/type_crews_over_time_cost_fight_variants.png", dpi=300)
plt.show()