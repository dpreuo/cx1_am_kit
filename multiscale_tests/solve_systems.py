from koala.pointsets import generate_random
from koala.voronization import generate_lattice
from koala.phase_space import k_hamiltonian_generator
from koala.flux_finder import find_flux_sector
from koala.graph_color import color_lattice
import numpy as np
import pickle
import scipy.linalg as la
import time
from tqdm import tqdm
import os

"""
Questions this code tries to answer:
 - Is the ground state always gapless? If not always then what proportion are gapless and does that proportion diminish with size?
 - If some are gapless, is that gaplessness always in one of the four toric code bits?
 - Does the difference between the flux averaged energy/gap diminish with system size?
 - Does the difference between each toric code sector gap/energy diminish as size goes up?
"""

if __name__ == '__main__':

    job_id = int(os.environ["PBS_ARRAY_INDEX"])
    # job_id = 4
    q_powers = np.arange(2, 7)
    k_resolution = 20

    # location = '/Users/perudornellas/python/imperial/cx1_am_kit/multiscale_tests/'
    location = '/rds/general/user/ppd19/home/cx1_am_kit/multiscale_tests/'
    J = np.array([1, 1, 1])

    with open(f'{location}run_params.pickle', 'rb') as f:
        plaquette_numbers = pickle.load(f)

    t_vals = []
    with open(f'{location}results/lattices/l{job_id}.pickle', 'wb') as f_lattices, open(f'{location}results/properties/p{job_id}.pickle', 'wb') as f_results:
        for p in tqdm(plaquette_numbers):
            t0 = time.time()
            points = generate_random(p)
            lattice = generate_lattice(points)
            coloring = color_lattice(lattice)
            s = np.array([plaq.n_sides for plaq in lattice.plaquettes])
            gnd_flux = (-(1j)**s).real + (-(1j)**s).imag
            ujk = find_flux_sector(lattice, gnd_flux)

            hk = k_hamiltonian_generator(lattice, coloring, ujk, J)

            k_values = np.arange(k_resolution)*2*np.pi/k_resolution
            KX, KY = np.meshgrid(k_values, k_values)
            k_vals = np.concatenate(
                [KX[:, :, np.newaxis], KY[:, :, np.newaxis]], axis=2)

            def solve_hk(k):
                h = hk(k)
                e = la.eigvalsh(h)
                return e

            e, v = la.eigh(hk([0, 0]))
            p_ratios = np.sum(
                np.abs(v[:, :, np.newaxis])**(2*q_powers), axis=0)

            e_values = np.apply_along_axis(solve_hk, 2, k_vals)

            t = time.time() - t0
            t_vals.append(t)

            pickle.dump(lattice, f_lattices)
            pickle.dump((e_values, p_ratios, t), f_results)

m, c = np.polyfit(np.log(plaquette_numbers), np.log(t_vals), 1)
print(m, c)
