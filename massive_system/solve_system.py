from koala.phase_space import k_hamiltonian_generator, analyse_hk
from koala.flux_finder import n_to_ujk_flipped
import pickle
import numpy as np
import os
from mpire import WorkerPool
import time
import datetime

if __name__ == '__main__':

    dir_location = '/rds/general/user/ppd19/home/cx1_am_kit/massive_system/'
    # dir_location = '/Users/perudornellas/python/imperial/cx1_am_kit/massive_system/'

    start_time = time.time()
    # job_id = 3
    job_id = int(os.environ["PBS_ARRAY_INDEX"]) - 1

    job_name = 'job_' + str(job_id + 1 )

    # load job info
    with open(dir_location + 'lattice_parameters.pickle', 'rb') as f:
        x = pickle.load(f)

    lattice = x['lattice']
    coloring = x['coloring']
    J = x['J_values']
    ujk = x['initial_ujk']
    start_and_end = x['start_and_finish_point'][job_id]
    min_spanning_set = x['spanning_tree']
    phase_resolution = x['phase_resolution']
    number_jobs_log = x['log_two_n_jobs']
    cores_per_batch = x['cores_per_batch']
    prog_bar = x['prog_bar']

    # now look over the subset of flux sectors we have been assigned
    def find_gap_energy_from_n(index_in):
        new_ujk = n_to_ujk_flipped(index_in, ujk, min_spanning_set)
        Hk = k_hamiltonian_generator(lattice, coloring,new_ujk,J)
        e, g = analyse_hk(Hk, phase_resolution)
        return (e,g)

    with WorkerPool(n_jobs=cores_per_batch) as pool:
        results = np.array(pool.map(
            find_gap_energy_from_n, 
            range(start_and_end[0], start_and_end[1]),
            progress_bar=prog_bar
            ))


    time_diff = time.time() - start_time
    print(f"Results generated, saving... --- {str(datetime.timedelta(seconds=time_diff))} ---")

    output = {
        'job_num': job_id, 
        'energies': results[:,0],
        'gaps': results[:,1],
        'start_finish': start_and_end
    }

    with open(dir_location + 'results/'+job_name+'.pickle' , 'wb') as f:
        pickle.dump(output,f)
    
    time_diff = time.time() - start_time
    print(f"Process finished --- {str(datetime.timedelta(seconds=time_diff))} ---")