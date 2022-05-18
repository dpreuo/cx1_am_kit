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

    # run at home
    location = '/Users/perudornellas/python/imperial/cx1_am_kit/state_scaling/'
    max_system_size = 30

    # run on cx1
    # max_system_size = 50
    # location = '/rds/general/user/ppd19/home/cx1_am_kit/state_scaling/'

 
    N = max_system_size**2
    number_of_scales = 500

    points_max = generate_random(N)
    j_vals = np.array([1,1,1])

    scales = np.linspace(0.2,1,number_of_scales)
    
    metaparameters = {
        'max_points': points_max,
        'j_vals': j_vals,
        'scales': scales
    }
    with open(location + 'systems.pickle', 'wb') as f:
        pkl.dump(metaparameters, f)

        # generate all the systems
        for s in tqdm(scales):
            scaled_points = scale_points_down(points_max, s)
            lattice = generate_lattice(scaled_points)
            coloring = color_lattice(lattice)
            all_sides = np.array([p.n_sides for p in lattice.plaquettes])
            gnd_flux_sector = -(1j)**all_sides; gnd_flux_sector = gnd_flux_sector.real + gnd_flux_sector.imag
            gnd_ujk =find_flux_sector(lattice, gnd_flux_sector)

            res_dict = (lattice, coloring, gnd_ujk, s)
        
            pkl.dump(res_dict, f)

    

