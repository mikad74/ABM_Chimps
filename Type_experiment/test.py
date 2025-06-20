from Type_model import Type_Model as Model
import matplotlib.pyplot as plt
import numpy as np

n_sim = 50
sim_length = 100
t = np.linspace(1, sim_length, sim_length)
cost_fight_values = [10, 20, 50, 100]
n_types = 4
n_types_names = ['Anxious', 'Show-off', 'Random', 'Resentful']

fig, axs = plt.subplots(2, 2, figsize=(16, 12))
axs = axs.flatten()

for idx, cost_fight in enumerate(cost_fight_values):
    data_track = []
    data_track_oases = []

    for i in range(n_sim):
        model = Model(10 * n_types, 20, n_types, 20, cost_fight=cost_fight)
        for j in range(sim_length):
            model.run()
        data_track.append(model.data_track[0])       # Crew data
        data_track_oases.append(model.data_track[1]) # Oasis data

    # Plot crew types over time
    for i in range(n_types):
        n_types_i = np.array([
            [len([crew for crew in step if crew.strat == i]) for step in sim]
            for sim in data_track
        ])
        mean_type_counts = np.mean(n_types_i, axis=0)
        axs[idx].plot(t, mean_type_counts, label=f"{n_types_names[i]}")

    # Compute and plot average oasis.resource over time
    oases_avg_resource_per_sim = np.array([
        [np.mean([oasis.resource for oasis in step]) if step else 0 for step in sim]
        for sim in data_track_oases
    ])
    n_oases_over_time = np.mean(oases_avg_resource_per_sim, axis=0)
    axs[idx].plot(t, n_oases_over_time, label='Avg Oasis Resources', linestyle='--', color='black')

    axs[idx].set_title(f'cost_fight = {cost_fight}')
    axs[idx].set_xlabel('Time')
    axs[idx].set_ylabel('Number of Agents / Resource')
    axs[idx].legend()

plt.tight_layout()
plt.savefig("Type_experiment/type_crews_over_time_cost_fight_variants.png", dpi=300)
plt.show()
