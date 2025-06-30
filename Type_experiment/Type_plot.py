from Type_model import Type_Model as Model
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

n_sim = 200
sim_length = 1000
t = np.linspace(1, sim_length, sim_length)
cost_fight_values = [20, 50]
resource_values = [25, 50, 75, 100]
n_types_names = ['Anxious', 'Agressive', 'Random', 'Resentful']
n_types = len(n_types_names)

fig, axs = plt.subplots(2, 1, figsize=(9, 7))
axs = axs.flatten()

for idx, cost_fight in enumerate(tqdm(cost_fight_values)):
    data_track = []
    data_track_oases = []
    food_per_chimp_ = []

    for i in range(n_sim):
        food_per_chimp = []
        model = Model(10 * n_types, 100, n_types, 20, resource_per_oasis = 100, cost_fight = cost_fight, resource_constant=100, seasons=True)
        for j in range(sim_length):
            model.run()
        data_track.append(model.data_track[0])
        data_track_oases.append(model.data_track[1])

    n_types_over_time = []
    for i in range(n_types):
        n_types_i = np.array([[len([crew for crew in step if crew.strat == i]) for step in sim] for sim in data_track])
        
        mean_values = np.mean(n_types_i, axis=0)
        std_values = np.std(n_types_i, axis=0)
        n_types_over_time.append(mean_values)
        axs[idx].plot(t, mean_values, label=f"{n_types_names[i]}")
        #axs[idx].fill_between(t, mean_values - std_values, mean_values + std_values, alpha=0.2)
        print(f"Final population for {n_types_names[i]}: {mean_values[-1]:.2f} +/- {std_values[-1]:.2f}")
    axs[idx].set_title(f'cost of fight = {cost_fight}, final pop = {sum([n_types_over_time[i][-1] for i in range(n_types)]):.2f}')
    axs[idx].set_xlabel('Time')
    if model.seasons:
        axs[idx].axvline(500, color='black', linestyle='--')
        axs[idx].axvline(800, color='black', linestyle='--')
        axs[idx].axvspan(500, 800, color='gray', alpha=0.05)
        #axs[idx].axvline(1100, color='black', linestyle='--')
        #axs[idx].axvline(1400, color='black', linestyle='--')
        #axs[idx].axvspan(1100, 1400, color='gray', alpha=0.05)
        #axs[idx].axvline(1700, color='black', linestyle='--')
        #axs[idx].axvline(2000, color='black', linestyle='--')
        #axs[idx].axvspan(1700, 2000, color='gray', alpha=0.05)
    axs[idx].set_ylabel('Number of Agents')
    axs[idx].legend()

plt.tight_layout()
plt.savefig("Type_experiment/type_crews_over_time_cost_fight_variants.png", dpi=300)
plt.show()

