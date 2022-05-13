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

if __name__ == '__main__':
    
    start_time = time.time()

    job_id = int(os.environ["PBS_ARRAY_INDEX"])
    prog_bar = True        # print a progress bar? (if yes you get weird warnings :\ )
    n_repetitions = 6       # how many systems do you want to solve per job
    cores_per_batch = 8     # how many cores can you count on having for each node

    # system parameters
    n_plaquettes = 16
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
            'spanning_tree': min_spanning_set}
        )

    with open(f'/rds/general/user/ppd19/home/kitaev_systems/many_systems/results/job_{job_id}.pickle', 'wb') as f:
        pickle.dump(output,f)
    
    time_diff = time.time() - start_time
    print(f"Process finished --- {str(datetime.timedelta(seconds=time_diff))} seconds ---")
