from Type_model import Type_Model as Model
import matplotlib.pyplot as plt
import numpy as np

n_sim = 500
sim_length = 1000
n_types = 2
t = np.linspace(1, sim_length, sim_length)
data_track = []

for i in range(n_sim):
    model = Model(20*n_types, 20, n_types, 20)
    for j in range(sim_length):
        model.run()
    data_track.append(model.data_track[0])

plt.figure(figsize=(10, 6))
n_types_over_time = []
for i in range(n_types):
    n_types_i = np.array([[len([crew for crew in step if crew.type == i]) for step in sim] for sim in data_track])
    n_types_over_time.append(np.mean(n_types_i, axis=0))
    plt.plot(t, n_types_over_time[i], label = f"Crews of type {i}")
plt.xlabel('Time')
plt.ylabel('Number of Agents')
plt.title('Number of Agents Over Time by Type')
plt.legend()
plt.savefig("type_crews_over_time_cf_10.png", dpi = 300)
plt.show()