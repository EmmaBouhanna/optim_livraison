#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 21:40:09 2020

@author: sophierossi
"""
from graphe import *

g = Garage (2.2728354, 48.8281142997349, 40, 60)
C = Camion(50, 0, 10000)

k = 10 # choose number of clients
#df, warehouses, parcels = create_graph_components(k)

# juste pour s'assurer que les distances fonctionnent
df = pd.read_csv("df_warehouses_and_clients_example.csv")
#df.drop(0,0,inplace=True)
l = df.values.tolist()

w = l[0:20]
c = l[20:]


# construction des entrepots à la main
warehouses = []
for i in range(len(w)):
    lat, long = w[i][0], w[i][1]
    capacity = 400000 #m^3
    max_vehicles = 50
    max_light = 30
    warehouses.append(Entrepot(lat, long, max_vehicles, max_light, capacity))

# construction des clients à la main

w = len(warehouses)
parcels = []
for i in range(len(c)):
    destination = [c[i][0], c[i][1]]
    # parcel's size is random
    size = 0.01*np.random.randint(1, 100) # parcel sizes range from 10 cm^3 to 1 m^3
    random_draw = np.random.randint(0, w)
    where_from = warehouses[random_draw]
    parcels.append(Colis(size, where_from, destination))



# matrice des distances


e1 = warehouses[0]
print(e1.lat)
c1 = parcels[0]


m = pd.read_csv("travel_times_array_example.csv").values.tolist()
l_0 = [[0.00, 424, 1513,	 1262, 831, 512, 1565, 1865,	 1189, 1641, 2436, 1816, 1431, 1759, 1522, 2330, 639, 743, 470, 1166, 976, 974, 2504, 2507, 2582, 2036, 779, 1153, 2378, 2257, 1351, 518, 768, 435, 1342, 2704, 1905, 894, 1886, 1399, 2149, 1016, 2475, 1412, 1779, 1760, 2262, 665, 865, 1056]]
matrice = l_0+m
print(len(matrice[0]))

def dist(n1: Node, n2: Node, df, dist_matrix = [[0.00, 424, 1513,	 1262, 831, 512, 1565, 1865,	 1189, 1641, 2436, 1816, 1431, 1759, 1522, 2330, 639, 743, 470, 1166, 976, 974, 2504, 2507, 2582, 2036, 779, 1153, 2378, 2257, 1351, 518, 768, 435, 1342, 2704, 1905, 894, 1886, 1399, 2149, 1016, 2475, 1412, 1779, 1760, 2262, 665, 865, 1056]]+ pd.read_csv("travel_times_array_example.csv").values.tolist()):
    l = df.values.tolist()
    coords = []
    for el in l:
        coords.append([el[0], el[1]])
        
    if isinstance(n1, Garage):
        dist = 0 
    elif isinstance(n2, Garage):
        dist = 0
    else:
        for el in l:
            if n1.lat == el[0] and n1.long == el[1]:
                i = coords.index([n1.lat, n1.long])
            if n2.lat == el[0] and n2.long == el[1]:
                j = coords.index([n2.lat, n2.long])
        dist = dist_matrix[i][j]
    return(dist)




d = dist(e1, c1.client, df)
print(d)
coords = []
for el in l:
    coords.append([el[0], el[1]])


       


G = Graph(g, warehouses, parcels, C)
G.make_graph()
G.generate_csv(df)







