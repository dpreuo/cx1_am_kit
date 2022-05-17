from koala.pointsets import generate_random
from matplotlib import pyplot as plt
import numpy as np
from koala.voronization import generate_lattice
from koala.graph_color import color_lattice
from koala.flux_finder import find_flux_sector
import pickle as pkl
from tqdm import tqdm

def scale_points_down(points, scaling:float):
    if not scaling > 0 or not scaling<=1:
        raise Exception('scaling needs to be between 0 and 1')
    points_scaled = points/scaling - np.array([1,1])*(1-scaling)/(2*scaling)
    points_in_region = np.where(np.prod((points_scaled < 1)*(points_scaled > 0), axis=1))[0]
    points_out = points_scaled[points_in_region]
    return points_out

# this code generates the set of points and sets the starting parameters for the rest of the calculation

if __name__ == '__main__':

    max_system_size = 30
    N = max_system_size**2

    points_max = generate_random(N)
    j_vals = np.array([1,1,1])

    flux_sectors_per_job = 1

    scales = np.linspace(0.2,1,500)
    
    location = '/rds/general/user/ppd19/home/cx1_am_kit/state_scaling'

    # generate all the systems
    all_systems = []
    for s in tqdm(scales):
        scaled_points = scale_points_down(points_max, s)
        lattice = generate_lattice(scaled_points)
        coloring = color_lattice(lattice)
        all_sides = np.array([p.n_sides for p in lattice.plaquettes])
        gnd_flux_sector = -(1j)**all_sides; gnd_flux_sector = gnd_flux_sector.real + gnd_flux_sector.imag
        gnd_ujk =find_flux_sector(lattice, gnd_flux_sector)

        res_dict = {
            'lattice': lattice,
            'coloring': coloring,
            'ground_state_ujk': gnd_ujk,
            'scale': s
        }
    
        all_systems.append(res_dict)

    output = {
        'max_points': points_max,
        'flux_sectors_per_job': flux_sectors_per_job,
        'j_vals': j_vals,
        'all_systems': all_systems
    }

    with open(location + 'systems.pickle', 'wb') as f:
        pkl.dump(output, f)