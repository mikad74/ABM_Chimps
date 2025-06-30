from Type_model import Type_Model as Model
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors

#***********to match the colorcode of the one-stage game**************
cmap = plt.get_cmap('tab10')
blauw = cmap(0)
oranje = cmap(1)
groen = cmap(2)
rood = cmap(3)
paars = cmap(4)

def quantile_counts_by_strategy(data_track, n_types, sim_length, q_low=0.33, q_high=0.66):
    """
    Returns three arrays of shape (n_types, sim_length) with the **average per-run**
    number of agents in the low / mid / high energy buckets.
    """
    # gather energies for every strategy, every timestep, all simulations pooled
    energies = [[[] for _ in range(sim_length)] for _ in range(n_types)]
    for sim in data_track:            # one simulation
        for t_idx, step in enumerate(sim):   # one timestep
            for crew in step:
                energies[crew.strat][t_idx].append(crew.energy)

    # now compute thresholds + counts
    low_counts  = np.zeros((n_types, sim_length))
    mid_counts  = np.zeros_like(low_counts)
    high_counts = np.zeros_like(low_counts)

    for s in range(n_types):
        for t_idx in range(sim_length):
            e_arr = np.asarray(energies[s][t_idx])
            if e_arr.size == 0:       # strategy extinct at this timestep
                continue
            q1, q2 = np.quantile(e_arr, [q_low, q_high])
            # boolean masks
            low_mask  = e_arr <  q1
            mid_mask  = (e_arr >= q1) & (e_arr < q2)
            high_mask = e_arr >= q2
            # average per simulation so curves match your old scaling
            low_counts[s, t_idx]  = low_mask.sum()  / n_sim
            mid_counts[s, t_idx]  = mid_mask.sum()  / n_sim
            high_counts[s, t_idx] = high_mask.sum() / n_sim

    return low_counts, mid_counts, high_counts

n_sim = 500 # default 500
sim_length = 1000 # default 1000
t = np.linspace(1, sim_length, sim_length)
cost_fight_values = [10, 20, 50, 100]
#n_types = 4
#n_types_names = ['Anxious', 'Show-off', 'Random', 'Resentful']
n_types = 5
n_types_names = ['Anxious', 'Show-off', 'Random', 'Resentful', 'Agressive']

fig, axs = plt.subplots(2, 2, figsize=(16, 12))
axs = axs.flatten()
fig2, axs2 = plt.subplots(2, 2, figsize=(16, 12))
axs2 = axs2.flatten()

for idx, cost_fight in enumerate(cost_fight_values):
    data_track = []

    for i in range(n_sim):
        model = Model(10* n_types, 20, n_types, 20, cost_fight=cost_fight)
        for j in range(sim_length):
            model.run(agressive=True, constant_win=False) # default is no arguments
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
    

    #*********EXTRA plot – absolute counts per energy-quantile per strategy***********

    low_c, mid_c, high_c = quantile_counts_by_strategy(
        data_track, n_types, sim_length)
 
    for s in range(n_types):
        base = (blauw, paars, groen, rood, oranje)[s]
        axs2[idx].plot(t, high_c[s], color=base, label=f'{n_types_names[s]} – high')
        axs2[idx].plot(t, mid_c[s], color=base, linestyle='--', label=f'{n_types_names[s]} – mid')
        axs2[idx].plot(t, low_c[s], color=base, linestyle=':', label=f'{n_types_names[s]} – low')
    axs2[idx].set_title(f'Counts by energy level (cost_fight = {cost_fight})')
    axs2[idx].set_xlabel('Time')
    axs2[idx].set_ylabel('Avg. # agents per simulation')
    axs2[idx].legend(ncol=3, fontsize='small')

#fig.tight_layout()
#fig.savefig("with_agressive_cost_win_F_cB10.png", dpi=300)
fig2.tight_layout()
fig2.savefig("with_agressive_cost_win_F_energies_en300.png", dpi=300)

'''
Naming of the plots:
- without agressive: the initial Balthazar's distiction between always retreating or sometimes attempting to fight, 
and never really attempting to show off (because cost of fight always deduced)
- with agressive: adding "agressive" type which is kind of third layer, it always fights, 
but the "show-off" also fights, no distinction between bluff and fight
- with agressive sophisticated: distinction between bluffing and fighting is introduced, no cost involved in bluffing, 1/2 chance of winning,
cost involved in fighting, same chance of winning, if other agent is agressive, you'd have to fight with prob 1/2
- with agressive constant win False: all the same as for "with agressive sophisticated", add conditioning the probability of
winning the fight on the energy of the crews
- with aggressive ... energies - visualize agents with low, medium and high energy reserves per type separately to trace if
energy level has an effect on survival
- with aggressive ... cB num - with cost of bluff at the level of num
'''