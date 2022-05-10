from koala.pointsets import generate_random
from koala.voronization import generate_lattice
from koala.phase_space import k_hamiltonian_generator, analyse_hk
from koala.graph_utils import plaquette_spanning_tree
from koala.flux_finder import n_to_ujk_flipped
from koala.graph_color import color_lattice
import numpy as np
import pickle

import os
job_id = int(os.environ["PBS_ARRAY_INDEX"])

# how many times you want to test a system
n_repetitions = 2

# system parameters
n_plaquettes = 14
J = np.array([1,1,1])
phase_resolution = 50


output = []
for rep in range(n_repetitions):

    # generate lattice
    points = generate_random(n_plaquettes)
    lattice = generate_lattice(points)
    ujk = np.full(lattice.n_edges, 1)
    coloring = color_lattice(lattice)

    # find the minimum spanning tree
    min_spanning_set = plaquette_spanning_tree(lattice)
    n_in_tree =  len(min_spanning_set)

    # we want the energy and gap size for every flux sector
    energies = []; gaps = []

    # search over every possible combination of ujk flips - looks exhaustively over the whole flux space
    for val in range(2**n_in_tree):
        new_ujk = n_to_ujk_flipped(val, ujk, min_spanning_set)
        Hk = k_hamiltonian_generator(lattice, coloring,new_ujk,J)
        e, g = analyse_hk(Hk, phase_resolution)
        energies.append(e)
        gaps.append(g)

    output.append(
        {'lattice': lattice,
        'energies': energies,
        'gaps': gaps,
        'spanning_tree': min_spanning_set}
    )

with open(f'/rds/general/user/tch14/home/many_systems/results/job_{job_id}.pickle', 'wb') as f:
    pickle.dump(output,f)