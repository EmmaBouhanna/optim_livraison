from graphe_copy import *
import optim_gen_copy
import warehouses_clients
g = Garage (2.2728354, 48.8281142997349, 40, 60)
c = Camion(50, 0, 10000)

k = 10 # choose number of clients
simulation_vrptw(g, c, k)