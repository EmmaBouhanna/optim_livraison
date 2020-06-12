from graphe import *

g = Garage (150, 50, 40, 60)
c = Camion(50, 0, 10000)
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
G = Graph(g, entrepots, points_relais, paquets, c)
G.make_graph()
G.garage.children[0].children
# trace_graph(G)
file_properties = G.generate_csv()
print(file_properties)
vehicle_capacity= file_properties.pop()

import pandas as pd
from optim_gen import run_vrptw, truck_division, decode_to_GPS
truck_div = truck_division(file_properties)
print(truck_div)

instances = [] #listes pour regrouper les résultats par entrepot
liste_res =[]

for (i, file) in enumerate(file_properties[::3]):
    instance = pd.read_csv(file)
    if instance.shape[0] >2 :
        instances += [instance]
    print(instance.head())
    max_vehicle = truck_div[i]
    instance_bis = instance.drop(['Unnamed: 0', 'Identifiant', 'latitude', 'longitude'], axis = 'columns')
    n = instance_bis.shape[1]
    number_of_points = n - 1
    number_of_clients = number_of_points - 1
    instance_bis.columns = ['demand'] + [i for i in range(number_of_points)]

    distance_matrix = instance_bis[[i for i in range(0,number_of_points)]] #prend la matrice des colonnes
    try :
        res = run_vrptw(instance_bis, distance_matrix, vehicle_capacity, max_vehicle, 1.0, 1.0, number_of_clients, 100, 0.4, 0.2, 10)
        liste_res.append(res)
    except Exception:
        print('Oooops') # only one package to deliver    

print(len(liste_res[0]),len(instances))
decode_to_GPS(liste_res, instances)

