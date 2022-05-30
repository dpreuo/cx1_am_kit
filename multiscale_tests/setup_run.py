from koala.pointsets import generate_random
from koala.voronization import generate_lattice
from koala.phase_space import k_hamiltonian_generator, analyse_hk, gap_over_phase_space
from koala.flux_finder import find_flux_sector
from koala.graph_color import color_lattice
from mpire import WorkerPool
import numpy as np
import pickle
import scipy.linalg as la
import datetime
from tqdm import tqdm
from matplotlib import pyplot as plt


if __name__ == '__main__':

    # big run
    # minimum_L = 5
    # maximum_L = 40  # maximum the computer can solve is about 50*50 - takes a while
    # n_steps = 40

    # small run
    minimum_L = 5
    maximum_L = 8  # maximum the computer can solve is about 50*50 - takes a while
    n_steps = 10

    location = '/Users/perudornellas/python/imperial/cx1_am_kit/multiscale_tests/'


    plaquette_n_lims = np.array([minimum_L, maximum_L])**2
    plaquette_numbers = np.logspace(np.log10(plaquette_n_lims[0]), np.log10(
        plaquette_n_lims[1]), n_steps).round().astype('int')

    # speed estimates
    m,c = 2.495591702938489, -10.584595582678062

    def f(s):
        return np.exp(c)*s**m

    total_time = np.sum(f(plaquette_numbers))
    print(f'We expect the run to take: {str(datetime.timedelta(seconds = total_time))}')

    

    with open(location + 'run_params.pickle', 'wb' ) as f:
        pickle.dump(plaquette_numbers, f)