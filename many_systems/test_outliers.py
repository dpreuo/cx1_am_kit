import imp
import os
import pickle
from koala.graph_color import color_lattice
from koala.phase_space import analyse_hk, k_hamiltonian_generator
import numpy as np
from koala import plotting as pl
from koala.flux_finder import n_to_ujk_flipped, fluxes_from_bonds
from matplotlib import pyplot as plt
from scipy import linalg as la
import random
import matplotlib
matplotlib.rcParams.update({'font.size': 13, 'text.usetex': True, 'font.family': 'serif', 'font.serif': ['Computer Modern']})

outliers_location = 'many_systems/outliers.pickle'
with open(outliers_location, 'rb') as f:
    x = pickle.load(f)

k_resolution = 50
n_exeptions = len(x)
fig, axes = plt.subplots(n_exeptions,3,figsize = (20,10))

for num,a in enumerate(x):
    print(f'Lattice chosen because: {a[1]}')

    lattice = a[0]['lattice']
    energies = a[0]['energies']
    gaps = a[0]['gaps']
    spanning_tree = a[0]['spanning_tree']

    coloring = color_lattice(lattice)

    # find the winning flux etc
    ujk = np.ones(lattice.n_edges)
    winner = np.argmin(energies)
    winning_ujk = n_to_ujk_flipped(winner, ujk, spanning_tree)
    fluxes = fluxes_from_bonds(lattice, winning_ujk)
    all_sides = np.array([plaq.n_sides for plaq in lattice.plaquettes])
    J = np.array([1,1,1])

    Hk = k_hamiltonian_generator(lattice, coloring, winning_ujk,J)
    k_values = np.arange(k_resolution)*2*np.pi/k_resolution
    KX,KY = np.meshgrid(k_values,k_values)
    k_vals = np.concatenate([KX[:,:,np.newaxis],KY[:,:,np.newaxis]],axis=2)

    def find_bands(k):
        h = Hk(k)
        vals = la.eigvalsh(h)
        return vals
    bands = np.apply_along_axis(find_bands,2,k_vals)


    

    for n in range(bands.shape[2]):
        r = random.random(); b = random.random(); g = random.random()
        color = (r, g, b)

        axes[num,0].plot(bands[:,:,n], c=color)
        axes[num,1].plot(bands[:,:,n].T, c=color)
        axes[num,0].set_ylim(-0.2,0.2)
        axes[num,1].set_ylim(-0.2,0.2)

    pl.plot_edges(lattice, ax = axes[num,2])
    pl.plot_plaquettes(lattice, all_sides%2,['white', 'grey'], ax = axes[num,2])

plt.show()