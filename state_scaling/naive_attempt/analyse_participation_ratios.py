from unittest import result
from koala.pointsets import generate_random
from matplotlib import pyplot as plt
import numpy as np
from koala.voronization import generate_lattice
from koala.graph_color import color_lattice
from koala.hamiltonian import generate_majorana_hamiltonian
from koala.flux_finder import find_flux_sector
from mpire import WorkerPool
import pickle as pkl


if __name__ == '__main__':

    energy_bins = 200
    dimensions = np.zeros([5,energy_bins])

    for enum,q in enumerate(range(2,7)):
        print(q)
        energy_range = 1.5
        
        energy_lims = np.linspace(-energy_range, energy_range, energy_bins + 1)
        bin_size = 2*energy_range/energy_bins
        # q = 3

        with open('state_scaling/naive_attempt/systems.pickle' , 'rb') as f:
            x = pkl.load(f)
            results = x['results']
            scales = x['scale_list']
            starting_points = x['starting_points']

        averaged_participations = np.full([len(results), energy_bins], 0.)

        for n,res in enumerate(results):
            energies = res[0]
            states = res[1]
            p_ratios = np.sum(np.abs(states)**(2*q), axis= 0)
            
            energy_bin_vals = (energies+1.5)//bin_size
            
            unique_values, unique_locations = np.unique(energy_bin_vals, return_index=True)
            unique_locations = np.append(unique_locations,len(energies))
            
            for u in range(energy_bins):
                indices_to_sum = np.where(energy_bin_vals == u)[0]
                if indices_to_sum.size == 0:
                    val = 0
                else:
                    val = np.average(p_ratios[indices_to_sum])
                averaged_participations[n,u] = val

        
        Dq_values = np.zeros(energy_bins)

        for n in range(energy_bins):

            put_together = np.array([np.log(scales), np.log(averaged_participations[:,n]) ])


            nonzero = np.where(averaged_participations[:,n] > 0)[0]
            put_together_cleaned = put_together[:,nonzero]

            if put_together_cleaned.size >0:
                p = np.polyfit(put_together_cleaned[0], put_together_cleaned[1], 1)
                gradient = p[0]
                Dq = - gradient /(q-1)  
                Dq_values[n] = Dq
                print(p)
                plt.scatter(put_together_cleaned[0], put_together_cleaned[1])
                f = np.poly1d(p)
                plt.plot(np.log(scales) , f(np.log(scales)))
                plt.title(f'Grad: {p[0]}')
                plt.show()

        dimensions[enum] = Dq_values

    e_centers = energy_lims[:-1] + 0.5*bin_size
    with open('state_scaling/naive_attempt/dimensions.pickle', 'wb') as f:
        pkl.dump((dimensions.T, e_centers), f)


        