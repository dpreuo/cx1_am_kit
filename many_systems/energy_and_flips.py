import os
import pickle
from traceback import print_tb
import numpy as np
from koala import plotting as pl
from koala.flux_finder import n_to_ujk_flipped, fluxes_from_bonds
from matplotlib import pyplot as plt
from koala.phase_space import analyse_hk, k_hamiltonian_generator
from koala.graph_color import color_lattice
from tqdm import tqdm
from mpire import WorkerPool

results_location = '/Users/perudornellas/python/imperial/cx1_am_kit/many_systems/results_anisotropic/'
files = [f for f in os.listdir(results_location) if not f.startswith('.')]

# load all the results
full_output = []
for filename in files:
    with open(results_location + filename, 'rb') as f:
        x = pickle.load(f)
        full_output = [*full_output, *x]

print(f'we have {len(full_output)} lattices to look at')


for n,result in enumerate(full_output):

    save_result = False
    flag = ''

    # load lattice
    lattice = result['lattice']
    energies = result['energies']
    gaps = result['gaps']
    spanning_tree = result['spanning_tree']
    
    # # find the winning flux etc
    ujk = np.ones(lattice.n_edges)
    winner = np.argmin(energies)
    lowest_energy = energies[winner]
    winning_ujk = n_to_ujk_flipped(winner, ujk, spanning_tree)
    winning_flux_1 = fluxes_from_bonds(lattice,winning_ujk, real=False)
    winning_flux_2 = winning_flux_1.conj()
    all_sides = np.array([ s.n_sides for s in lattice.plaquettes])

    flux_densities = []
    for index in np.arange(len(energies)):
        current_ujk = n_to_ujk_flipped(index, ujk, spanning_tree)
        current_flux = fluxes_from_bonds(lattice,current_ujk, real=False)

        nf1 = np.sum(current_flux != winning_flux_1)
        nf2 = np.sum(current_flux != winning_flux_2)
        flux_density = np.min([nf1, nf2])
        flux_densities.append(flux_density)

    e_offsets = energies - lowest_energy
    plt.scatter(flux_densities,e_offsets)
    plt.show()
    
