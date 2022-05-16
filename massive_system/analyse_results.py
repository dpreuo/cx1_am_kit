import os
import pickle
from traceback import print_tb
import numpy as np
from koala import plotting as pl
from koala.phase_space import analyse_hk,gap_over_phase_space, k_hamiltonian_generator
from koala.flux_finder import n_to_ujk_flipped, fluxes_from_bonds
from matplotlib import pyplot as plt
from pytest import fail

results_location = 'massive_system/results/'

# load the system
with open('massive_system/lattice_parameters.pickle', 'rb') as f:
    x = pickle.load(f)

lattice = x['lattice']
coloring = x['coloring']
J = x['J_values']
ujk = x['initial_ujk']
min_spanning_set = x['spanning_tree']
phase_resolution = x['phase_resolution']


# load all the results
full_output = []
for filename in os.listdir(results_location):
    with open(results_location + filename, 'rb') as f:
        x = pickle.load(f)
    full_output.append(x)

number_ranges = np.array([x['start_finish'][0] for x in full_output])
order = np.argsort(number_ranges)
reordered_results = np.array(full_output)[order]

all_energies = np.concatenate([r['energies'] for r in reordered_results])
all_gaps = np.concatenate([r['gaps'] for r in reordered_results])

# plt.plot(all_energies)
# plt.show()

winning_index = np.argmin(all_energies)

winning_ujk = n_to_ujk_flipped(winning_index, ujk, min_spanning_set)
gnd_state_flux = fluxes_from_bonds(lattice,winning_ujk)
all_sides = np.array([p.n_sides for p in lattice.plaquettes])

sides_sort = np.argsort(all_sides)

def lieb_check(flux, side):
    guess1 = -(1j)**side
    guess2 = -(-1j)**side

    guess1 = (guess1.real + guess1.imag).astype('int') 
    guess2 = (guess2.real + guess2.imag).astype('int') 

    out = False
    if flux == guess1 or flux == guess2:
        out = True

    return out
fail_flag = False
for f, s in zip(gnd_state_flux, all_sides):
    if not lieb_check(f,s):
        fail_flag = True
if fail_flag:
    print(f'Lieb check FAILED')
else:
    print('Lieb check passed')

print(f'Ground state energy: {all_energies[winning_index]}\nGround State gap: {all_gaps[winning_index]}')

Hk = k_hamiltonian_generator(lattice,coloring,winning_ujk,J)
gaps = gap_over_phase_space(Hk, 50,False)

e_sort = np.argsort(all_energies)
gaps_sorted = all_gaps[e_sort]
energies_sorted = all_energies[e_sort]

fig, axes = plt.subplots(2,2)
axes[0,0].plot(energies_sorted[:100])
axes[1,0].plot(gaps_sorted[:100])

axes[0,1].matshow(gaps)
axes[0,1].set_title('Gap over phase space')
plt.show()

# export the results for tom
