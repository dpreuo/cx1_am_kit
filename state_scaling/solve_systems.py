from koala.pointsets import generate_random
from matplotlib import pyplot as plt
import numpy as np
from koala.voronization import generate_lattice
from koala.graph_color import color_lattice
from koala.hamiltonian import generate_majorana_hamiltonian
from koala.flux_finder import find_flux_sector
from mpire import WorkerPool
import pickle as pkl
import os
from mpire import WorkerPool

if __name__ == '__main__':

    job_id = int(os.environ["PBS_ARRAY_INDEX"]) 
    input_location = 'state_scaling/systems.pickle'
    results_location = 'state_scaling/results/'

    with open(input_location, 'rb') as f:
        x = pkl.load(f)
        max_points = x['max_points']
        flux_sectors_per_job = x['flux_sectors_per_job']
        j_vals = x['j_vals']
        all_systems = x['all_systems']
        del x

    def analyse_system(n):
        system = all_systems[n]
        l = system['lattice']
        coloring = system['coloring']
        ujk = 1 - 2*np.random.randint(0,2,l.n_edges)
        hamiltonian = generate_majorana_hamiltonian(l, coloring, ujk, j_vals)

        return np.linalg.eigh(hamiltonian), ujk

    all_solved_systems = []
    for round in range(flux_sectors_per_job):
        with WorkerPool(n_jobs=8) as pool:
            solved_systems = pool.map(analyse_system, range(len(all_systems)), progress_bar=True)
        all_solved_systems.append(solved_systems)
    
    with open(results_location + f'job_{job_id}.pickle', 'wb') as f:
        pkl.dump(all_solved_systems)

    