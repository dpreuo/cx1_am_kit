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
from tqdm import tqdm


if __name__ == '__main__':

    # run at home
    # job_id = 3
    # input_location = '/Users/perudornellas/python/imperial/cx1_am_kit/state_scaling/systems.pickle'
    # results_location = '/Users/perudornellas/python/imperial/cx1_am_kit/state_scaling/results/'

    # run on cx1
    job_id = int(os.environ["PBS_ARRAY_INDEX"]) 
    input_location = '/rds/general/user/ppd19/home/cx1_am_kit/state_scaling/systems.pickle'
    results_location = '/rds/general/user/ppd19/home/cx1_am_kit/state_scaling/results/'

    with open(input_location, 'rb') as f_in:

        # load the metaparameters
        metaparmeters = pkl.load(f_in)
        points_max = metaparmeters['max_points'] 
        j_vals = metaparmeters['j_vals'] 
        scales = metaparmeters['scales']
        number_of_scales = len(scales)  

        with open(results_location + f'job_{job_id}.pickle', 'wb') as f:

            # for each scale, solve the hamiltonian and dump the result
            for n in tqdm(range(number_of_scales)):

                lattice, coloring, gnd_ujk, s = pkl.load(f_in)
                ujk = 1 - 2*np.random.randint(0,2,lattice.n_edges)
                hamiltonian = generate_majorana_hamiltonian(lattice, coloring, ujk, j_vals)
                e,v = np.linalg.eigh(hamiltonian)
                output = {
                    'system_index': n,
                    'energies': e,
                    'eigenstates': v,
                    'ujk': ujk
                }
                pkl.dump(output,f)


    
