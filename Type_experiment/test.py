from Type_model import Type_Model as Model
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

n_sim = 150
sim_length = 3000
t = np.linspace(1, sim_length, sim_length)

flexible_values = [.5, 1, 3]
ram_values = [5, 10, 15]
n_types_names = ['Anxious', 'Agressive', 'Random', 'Resentful', 'Flexible']
n_types = len(n_types_names)

fig, axs = plt.subplots(3, 3, figsize=(18, 14), sharex=True, sharey=True)

for row_idx, ram in enumerate(tqdm(ram_values, desc="RAM values")):
    for col_idx, flexible in enumerate(tqdm(flexible_values, desc="Flexible values", leave=False)):

        data_track = []

        for i in range(n_sim):
            model = Model(
                10 * n_types, 
                100, 
                n_types, 
                20,
                resource_per_oasis=100,
                cost_fight=20,  # Or any constant or looped value you want
                resource_constant=100,
                seasons=True,
                flexible=flexible,
                ram=ram
            )
            for j in range(sim_length):
                model.run()
            data_track.append(model.data_track[0])

        ax = axs[row_idx, col_idx]
        n_types_over_time = []

        for type_idx in range(n_types):
            n_types_i = np.array([
                [len([crew for crew in step if crew.strat == type_idx]) for step in sim] 
                for sim in data_track
            ])

            mean_values = np.mean(n_types_i, axis=0)
            std_values = np.std(n_types_i, axis=0)
            n_types_over_time.append(mean_values)
            
            ax.plot(t, mean_values, label=f"{n_types_names[type_idx]}")
            #ax.fill_between(t, mean_values - std_values, mean_values + std_values, alpha=0.2)

        ax.set_title(f"flexible={flexible}, ram={ram}")
        if model.seasons:
            ax.axvline(500, color='black', linestyle='--')
            ax.axvline(800, color='black', linestyle='--')
            ax.axvspan(500, 800, color='gray', alpha=0.05)
            ax.axvline(1100, color='black', linestyle='--')
            ax.axvline(1400, color='black', linestyle='--')
            ax.axvspan(1100, 1400, color='gray', alpha=0.05)
            ax.axvline(1700, color='black', linestyle='--')
            ax.axvline(2000, color='black', linestyle='--')
            ax.axvspan(1700, 2000, color='gray', alpha=0.05)

        if row_idx == 2:
            ax.set_xlabel("Time")
        if col_idx == 0:
            ax.set_ylabel("Number of Agents")
        if row_idx == 0 and col_idx == 2:
            ax.legend(loc='upper right', fontsize=8)

plt.tight_layout()
plt.savefig("Type_experiment/type_crews_over_time_flexible_ram_grid2.png", dpi=300)
plt.show()
