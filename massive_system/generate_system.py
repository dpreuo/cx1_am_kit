from distutils import core
from koala.pointsets import generate_random
from koala.voronization import generate_lattice
from koala.phase_space import k_hamiltonian_generator, analyse_hk
from koala.flux_finder import n_to_ujk_flipped
from koala.graph_utils import plaquette_spanning_tree
from koala.graph_color import color_lattice
import numpy as np
import pickle

if __name__ == '__main__':
    # job parameters
    phase_resolution = 50
    n_plaquettes = 26
    number_of_jobs = 512
    cores_per_batch = 8
    prog_bar = True
    J = np.array([1,1,1])
    
    dir_location = '/rds/general/user/ppd19/home/cx1_am_kit/massive_system/'        #run at cx1
    # dir_location = '/Users/perudornellas/python/imperial/cx1_am_kit/massive_system/'      #run at home

    job_power = int(np.log2(number_of_jobs))
    if np.abs(job_power - np.log2(number_of_jobs)) >= 1e-5:
        raise Exception('number_of_jobs must be a power of 2')

    # generate lattice
    points = generate_random(n_plaquettes)
    lattice = generate_lattice(points)

    # set ujk and colour
    ujk = np.full(lattice.n_edges, 1)
    coloring = color_lattice(lattice)

    # find spanning tree
    min_spanning_set = plaquette_spanning_tree(lattice)
    n_in_tree =  len(min_spanning_set)

    # calculate how many flux sectors each job looks at
    pow_two_per_job = n_in_tree-job_power

    jobs_array = np.arange(number_of_jobs)
    start_point_per_job = (2**pow_two_per_job)*jobs_array
    finish_point_per_job = start_point_per_job + 2**pow_two_per_job

    # a list of the start and end inxed for flux sector for each job that gets executed
    start_and_finish_point  = [(s,f) for s,f in zip(start_point_per_job,finish_point_per_job)]

    print(f'This run will produce on the order of {24*(2**n_in_tree) / 1e6 :.0f} Mb of data')

    output = {
        'lattice': lattice,
        'coloring': coloring,
        'J_values': J,
        'initial_ujk': ujk,
        'spanning_tree':min_spanning_set,
        'start_and_finish_point': start_and_finish_point,
        'phase_resolution': phase_resolution,
        'log_two_n_jobs': job_power,
        'cores_per_batch': cores_per_batch,
        'prog_bar': prog_bar,
    }

    with open(dir_location + 'lattice_parameters.pickle', 'wb') as f:
        pickle.dump(output,f)
