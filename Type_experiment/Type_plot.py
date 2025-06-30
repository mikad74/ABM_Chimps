from Type_model import Type_Model as Model
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from pathlib import Path

#***********ADJUST THESE************
out_text_name = "without_aggressive.txt" #give a good name to your output, suggested convention - see at the end of this .py
name_graphs = "without_aggressive_en300.png" #give a name to the .png with graphs of the results
run_args = dict(
    agressive = False, # default for base model with only 4 types, adds Show-Off if True
    constant_win=True, # default for constant prob_win that is independent of size, makes fight dependent on size if False
    cost_bluff = 0 # default is no cost, but you can pass some cost to see if the dynamics changes
)

#***********to match the colorcode of the one-stage game**************
cmap = plt.get_cmap('tab10')
blauw = cmap(0)
oranje = cmap(1)
groen = cmap(2)
rood = cmap(3)
paars = cmap(4)

n_sim = 500 # default 500
sim_length = 1000 # default 1000
t = np.linspace(1, sim_length, sim_length)
cost_fight_values = [10, 20, 50, 100] 
#n_types = 4  #use these to reproduce the basic one-stage game with only 4 types of agents
#n_types_names = ['Anxious', 'Aggressive', 'Random', 'Resentful'] #and this too
n_types = 5
n_types_names = ['Anxious', 'Show-off', 'Random', 'Resentful', 'Aggressive']

out_file = Path(out_text_name).open("w") 
fig, axs = plt.subplots(2, 2, figsize=(16, 12))
axs = axs.flatten()

for idx, cost_fight in enumerate(cost_fight_values):
    data_track = []

    for i in range(n_sim):
        model = Model(10* n_types, 20, n_types, 20, cost_fight=cost_fight)
        for j in range(sim_length):
            model.run(**run_args) 
        data_track.append(model.data_track[0])


    for i in range(n_types):
        n_types_i = np.array([[len([crew for crew in step if crew.strat == i]) for step in sim] for sim in data_track])
        m = np.mean(n_types_i, axis=0)
        se = np.std(n_types_i, axis=0, ddof=1) / np.sqrt(n_sim)
        ci = 1.96 * se

        c = (blauw, paars, groen, rood, oranje)[i] #comment this for one-stage game
            
        axs[idx].plot(t, m, color = c, label=f"{n_types_names[i]}") 
        axs[idx].fill_between(t, m-ci, m+ci, color = c, alpha=0.2)  
        
        final_vals = n_types_i[:, -1]   
        m_final    = final_vals.mean()    # mean survivors
        sd_final   = final_vals.std(ddof=1)   # SD 
        ci_final   = 1.96 * sd_final / np.sqrt(n_sim)   # 95 % CI
        out_file.write(f"{n_types_names[i]:<10}  "
                       f"mean={m_final:5.2f}  "
                       f"SD={sd_final:5.2f}  "
                       f"95%CI=±{ci_final:4.2f}\n")

    axs[idx].set_title(f'cost_fight = {cost_fight}')
    axs[idx].set_xlabel('Time')
    axs[idx].set_ylabel('Number of Agents')
    axs[idx].legend()

plt.tight_layout()
plt.savefig(name_graphs, dpi=300) #naming convention below
plt.show()

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
- with aggressive ... energies - go to Type plot conditioned
- with aggressive ... cB num - with cost of bluff at the level of num
'''