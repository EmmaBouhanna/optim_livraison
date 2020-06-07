from graphe import *

g = Garage (150, 50, 40, 60)
e1 = Entrepot (100, 100, 10, 15, 5000)
e2 = Entrepot (200, 100, 20, 10, 4000)
e3 = Entrepot (100, 300, 15, 15, 4000)
p1 = Colis (20, e1, [104, 120])
p2 = Colis (30, e1, [104, 135])
p3 = Colis (15, e2, [100, 135])
p4 = Colis (23, e2, [103, 123])
p5 = Colis (12, e1, [112, 122])
p6 = Colis (13, e1, [107, 108])
p7 = Colis (25, e3, [133, 123])
entrepots = [e1, e2, e3]
points_relais = []
paquets = [p1, p2, p3, p4, p5, p6, p7]
G = Graph(g, entrepots, points_relais, paquets)
G.make_graph()
G.garage.children[0].children
# trace_graph(G)
file_names = G.generate_csv(g)
camions_garage = file_names.pop()


import pandas as pd
from optim_gen import run_vrptw
for file in file_names:

    instance = pd.read_csv(file)
    instance.drop(['Unnamed: 0', 'Identifiant', 'latitude', 'longitude'], axis = 'columns', inplace = True)
    n = instance.shape[1]
    number_of_points = n - 3
    number_of_clients = number_of_points - 1
    instance.columns = ['vehicle_capacity', 'max_vehicle', 'demand'] + [i for i in range(number_of_points)]
    print(instance.head())

    distance_matrix = instance[[i for i in range(0,number_of_points)]] #prend la matrice des colonnes
    print(distance_matrix.head())

    run_vrptw(instance, distance_matrix, 1.0, 1.0, number_of_clients, 100, 0.4, 0.2, 10)
