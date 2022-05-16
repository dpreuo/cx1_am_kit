from koala.pointsets import generate_random
from matplotlib import pyplot as plt
import numpy as np
from koala.voronization import generate_lattice
from koala.graph_color import color_lattice
from koala.hamiltonian import generate_majorana_hamiltonian
from koala.flux_finder import find_flux_sector
from mpire import WorkerPool
import pickle as pkl

# this code doesnt use any cx1 stuff - just see how far you can get on your laptop

if __name__ == '__main__':
    max_system_size = 50

    N = max_system_size**2

    points_max = generate_random(N)

    def scale_points_down(points, scaling:float):
        if not scaling > 0 or not scaling<=1:
            raise Exception('scaling needs to be between 0 and 1')
        points_scaled = points/scaling - np.array([1,1])*(1-scaling)/(2*scaling)
        points_in_region = np.where(np.prod((points_scaled < 1)*(points_scaled > 0), axis=1))[0]
        points_out = points_scaled[points_in_region]
        return points_out

    j_vals = np.array([1,1,1])

    def find_scaled_solutions(scale):
        scaled_points = scale_points_down(points_max, scale)
        lattice = generate_lattice(scaled_points)
        coloring = color_lattice(lattice)
        all_sides = np.array([p.n_sides for p in lattice.plaquettes])
        gnd_flux_sector = -(1j)**all_sides; gnd_flux_sector = gnd_flux_sector.real + gnd_flux_sector.imag
        gnd_ujk =find_flux_sector(lattice, gnd_flux_sector) 

        H = generate_majorana_hamiltonian(lattice, coloring, gnd_ujk, j_vals)
        eigs, states = np.linalg.eigh(H)
        return (eigs, states)

    scale_list = list(np.linspace(1,0.2,500))

    with WorkerPool(n_jobs=8) as pool:
        results = pool.map(find_scaled_solutions, scale_list, progress_bar=True)

    out = {'results': results, 'scale_list': scale_list, "starting_points": points_max}

    with open('state_scaling/naive_attempt/systems.pickle', 'wb') as f:
        pkl.dump(out, f)