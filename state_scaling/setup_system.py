from koala.pointsets import generate_random
from matplotlib import pyplot as plt
import numpy as np
from koala.voronization import generate_lattice
from koala.graph_color import color_lattice
from koala.hamiltonian import generate_majorana_hamiltonian
from koala.flux_finder import find_flux_sector
from mpire import WorkerPool

if __name__ == '__main__':
    max_system_size = 50
    N = max_system_size**2