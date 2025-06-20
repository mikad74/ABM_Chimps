from Type_model import Type_Model as Model
import matplotlib.pyplot as plt
import numpy as np

print("hahaha")

n_sim = 500
sim_length = 1000
t = np.linspace(1, sim_length, sim_length)
cost_fight_values = [10, 20, 50, 100]
n_types = 4
n_types_names = ['Anxious', 'Show-off', 'Random', 'Resentful']
cost_fight_values = [10, 20, 50, 100]

fig, axs = plt.subplots(2, 2, figsize=(16, 12))
axs = axs.flatten()

for idx, cost_fight in enumerate(cost_fight_values):
    data_track = []

    for i in range(n_sim):
        model = Model(10* n_types, 20, n_types, 20, cost_fight=cost_fight)
        for j in range(sim_length):
            model.run()
        data_track.append(model.data_track[0])

    n_types_over_time = []
    for i in range(n_types):
        n_types_i = np.array([[len([crew for crew in step if crew.strat == i]) for step in sim] for sim in data_track])
        n_types_over_time.append(np.mean(n_types_i, axis=0))
        axs[idx].plot(t, n_types_over_time[i], label=f"{n_types_names[i]}")

    axs[idx].set_title(f'cost_fight = {cost_fight}')
    axs[idx].set_xlabel('Time')
    axs[idx].set_ylabel('Number of Agents')
    axs[idx].legend()

plt.tight_layout()
plt.savefig("Type_experiment/type_crews_over_time_cost_fight_variants.png", dpi=300)
plt.show()