from cProfile import label
from matplotlib import pyplot as plt
import numpy as np
import pickle as pkl

if __name__ == '__main__':

    with open('state_scaling/naive_attempt/dimensions.pickle', 'rb') as f:
        dims, energies = pkl.load(f)

    with open('state_scaling/naive_attempt/systems.pickle', 'rb') as f:
        x = pkl.load(f)
        results = x['results']

    ex = results[0][0]
    fix,axes = plt.subplots(2,1)

    plt.sca(axes[0])
    plt.title('Density of states')
    plt.hist(ex, bins = len(energies),density=True)
    plt.xlabel('Energy')
    plt.sca(axes[1])
    plt.title('Averaged fractal dimension over the spectrum')
    plt.plot(energies, dims,label= ['q = 2', 'q = 3', 'q = 4', 'q = 5', 'q = 6'])
    plt.legend()
    plt.xlabel('Energy')
    plt.ylabel('$D_q$ = $tau_q$/(q-1)')
    plt.show()