from graphe_sans_osmnx import *
from optim_gen import simulation_vrptw
g = Garage (2.2728354, 48.8281142997349, 40, 60)
c = Camion(50, 0, 10000)

k = 30 # choose number of clients
simulation_vrptw(g, c, k)