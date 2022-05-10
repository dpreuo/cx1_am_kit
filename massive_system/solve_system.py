from koala.phase_space import k_hamiltonian_generator, analyse_hk
from koala.flux_finder import n_to_ujk_flipped
import pickle
import numpy as np
import os
job_id = int(os.environ["PBS_ARRAY_INDEX"])

job_name = 'job_' + str(job_id)

# load job info
with open('massive_system/lattice_parameters', 'rb') as f:
    x = pickle.load(f)

lattice = x['lattice']
coloring = x['coloring']
J = x['J_values']
ujk = x['initial_ujk']
start_and_end = x['start_and_finish_point'][job_id]
min_spanning_set = x['spanning_tree']
phase_resolution = x['phase_resolution']
number_jobs_log = x['log_two_n_jobs']

# now look over the subset of flux sectors we have been assigned
energies = []; gaps = []
for val in range(start_and_end[0], start_and_end[1]):
    new_ujk = n_to_ujk_flipped(val, ujk, min_spanning_set)
    Hk = k_hamiltonian_generator(lattice, coloring,new_ujk,J)
    e, g = analyse_hk(Hk, phase_resolution)
    energies.append(e)
    gaps.append(g)

gaps = np.array(gaps)
energies = np.array(energies)

output = {
    'job_num': job_id, 
    'energies': energies, 
    'gaps': gaps,
    'start_finish': start_and_end
}

with open('massive_system/results/'+job_name , 'wb') as f:
    pickle.dump(output,f)