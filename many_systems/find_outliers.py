import os
import pickle
from traceback import print_tb
import numpy as np
from koala import plotting as pl
from koala.flux_finder import n_to_ujk_flipped, fluxes_from_bonds
from matplotlib import pyplot as plt

results_location = 'many_systems/results/'

# load all the results
full_output = []
for filename in os.listdir(results_location):
    with open(results_location + filename, 'rb') as f:
        x = pickle.load(f)
        full_output = [*full_output, *x]

print(f'we have {len(full_output)} lattices to look at')

def lieb_check(flux, side):
    guess1 = -(1j)**side
    guess2 = -(-1j)**side

    guess1 = (guess1.real + guess1.imag).astype('int') 
    guess2 = (guess2.real + guess2.imag).astype('int') 

    out = False
    if flux == guess1 or flux == guess2:
        out = True

    return out

weird_lattices = []
for n,result in enumerate(full_output):

    save_result = False
    flag = ''

    # load lattice
    lattice = result['lattice']
    energies = result['energies']
    gaps = result['gaps']
    spanning_tree = result['spanning_tree']
    
    # find the winning flux etc
    ujk = np.ones(lattice.n_edges)
    winner = np.argmin(energies)
    winning_ujk = n_to_ujk_flipped(winner, ujk, spanning_tree)
    fluxes = fluxes_from_bonds(lattice, winning_ujk)
    all_sides = np.array([plaq.n_sides for plaq in lattice.plaquettes])

    # check lieb result
    for f, s in zip(fluxes, all_sides):
        if not lieb_check(f,s):
            print(f'index {n:04d} --- Fails Lieb check!!!!!')
            save_result = True
            flag = flag + ' wrong ground state '
            
    
    # check gaps
    g = gaps[winner]
    if g<1e-10:
        print(f'index {n:04d} --- gap: {g:.2E}')
        save_result = True
        flag = flag + ' Gapless '
    
    if save_result:
        weird_lattices.append(
            (result,flag)
        )
    
with open('/Users/perudornellas/python/imperial/cx1_am_kit/many_systems/outliers.pickle', 'wb') as f:
    pickle.dump(weird_lattices, f)

    
