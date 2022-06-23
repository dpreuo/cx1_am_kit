from random import random
from koala.pointsets import generate_random
from koala.voronization import generate_lattice
from koala.phase_space import k_hamiltonian_generator, analyse_hk
from koala.graph_utils import plaquette_spanning_tree
from koala.flux_finder import n_to_ujk_flipped
from koala.graph_color import color_lattice
from mpire import WorkerPool
import numpy as np
import pickle
import os
import time
import datetime

def generate_J():
    # generate a random set of j values on the sum J = 1 triangle
    xy = np.random.rand(2)
    x0 = np.array([1,0,0])
    x1 = np.array([-1,1,1])
    v1 = np.array([-1,1,0])
    v2 = np.array([-1,0,1])
        
    if sum(xy) <= 1 :
        return x0 + xy[0]*v1 + xy[1]*v2
    else: 
        return x1 - xy[0]*v1 - xy[1]*v2

if __name__ == '__main__':
    
    start_time = time.time()

    # random j values 
    J = generate_J()

    # run at home
    # job_id = 1      # int(os.environ["PBS_ARRAY_INDEX"])
    # prog_bar = True        # print a progress bar? (if yes you get weird warnings :\ )
    # n_repetitions = 10      # how many systems do you want to solve per job
    # cores_per_batch = 8     # how many cores can you count on having for each node
    # save_location = f'/Users/perudornellas/python/imperial/cx1_am_kit/many_systems_random_j/results/'
    # n_plaquettes = 8
    
    # run at cx1
    job_id = int(os.environ["PBS_ARRAY_INDEX"])
    prog_bar = True        # print a progress bar? (if yes you get weird warnings :\ )
    n_repetitions = 6       # how many systems do you want to solve per job
    cores_per_batch = 8     # how many cores can you count on having for each node
    save_location = f'/rds/general/user/ppd19/home/cx1_am_kit/many_systems_random_j/results/'
    n_plaquettes = 16



    # system parameters
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

        def find_gap_energy_from_n(index_in):
            new_ujk = n_to_ujk_flipped(index_in, ujk, min_spanning_set)
            Hk = k_hamiltonian_generator(lattice, coloring,new_ujk,J)
            e, g = analyse_hk(Hk, phase_resolution)
            return (e,g)

        with WorkerPool(n_jobs=cores_per_batch) as pool:
            results = np.array(pool.map(
                find_gap_energy_from_n, 
                range(2**n_in_tree),
                progress_bar=prog_bar
                ))

        output.append(
            {'lattice': lattice,
            'energies': results[:,0],
            'gaps': results[:,1],
            'spanning_tree': min_spanning_set,
            'coloring': coloring,
            'J': J}
        )

    with open(f'{save_location}job_{job_id}.pickle', 'wb') as f:
        pickle.dump(output,f)
    
    time_diff = time.time() - start_time
    print(f"Process finished --- {str(datetime.timedelta(seconds=time_diff))} seconds ---")
