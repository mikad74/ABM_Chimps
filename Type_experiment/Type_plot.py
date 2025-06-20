from Type_model import Type_Model as Model
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

n_sim = 10
sim_length = 1000
t = np.linspace(1, sim_length, sim_length)
cost_fight_values = [10, 20, 50, 100]
n_types_names = ['Anxious', 'Show-off', 'Random', 'Resentful']
n_types = len(n_types_names)

fig, axs = plt.subplots(2, 2, figsize=(16, 12))
axs = axs.flatten()

for idx, cost_fight in enumerate(tqdm(cost_fight_values)):
    data_track = []
    data_track_oases = []
    food_per_chimp_ = []

    for i in range(n_sim):
        food_per_chimp = []
        model = Model(10* n_types, 20, n_types, cost_fight=cost_fight, oasis_spawn_proportional=True, abundance_factor=6, oasis_density=.24, food_consumption_speed=.33)
        for j in range(sim_length):
            model.run()
            if [crew for crew in model.crews.values()]:
                food_per_chimp.append(sum([oasis.resource for oasis in model.oases.values()])/sum([crew.crew_size for crew in model.crews.values()]))
            else:
                food_per_chimp.append(0)
        data_track.append(model.data_track[0])
        data_track_oases.append(model.data_track[1])
        food_per_chimp_.append(food_per_chimp)

    n_types_over_time = []
    for i in range(n_types):
        n_types_i = np.array([[len([crew for crew in step if crew.strat == i]) for step in sim] for sim in data_track])
        
        n_types_over_time.append(np.mean(n_types_i, axis=0))
        axs[idx].plot(t, n_types_over_time[i], label=f"{n_types_names[i]}")
    food_per_chimp = np.array(food_per_chimp_)
    food_per_chimp_overtime = np.mean(food_per_chimp, axis=0)
    axs[idx].plot(t, food_per_chimp_overtime, label='Food per Chimp', linestyle=':', color='orange')
    axs[idx].set_title(f'cost_fight = {cost_fight}')
    axs[idx].set_xlabel('Time')
    axs[idx].set_ylabel('Number of Agents')
    axs[idx].legend()

plt.tight_layout()
plt.savefig("Type_experiment/type_crews_over_time_cost_fight_variants.png", dpi=300)
plt.show()