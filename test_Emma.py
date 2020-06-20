from graphe import *
from optim_gen import results_vrptw
g = Garage (2.2728354, 48.8281142997349, 40, 60)
c = Camion(50, 0, 10000)

k = 10 # choose number of clients
results_vrptw(g, c, k)