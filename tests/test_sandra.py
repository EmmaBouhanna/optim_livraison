#Importations
import osmnx as ox
import networkx as nx
import numpy as np
import pandas as pd
import random
import folium

from warehouses_clients import *
from routes import *


## Test - 20 entrepôts, 30 clients

df_1 = pd.read_csv("warehouses.csv", sep=";")
df_complete = random_clients(30, df_1)[0]
coord_, tableau_, itineraires_ = itineraries(df_complete, critere_optim="travel_time")

# ==> beaucoup trop long à exécuter ! 
# En attendant de trouver une solution, on sauvegarde les données calculées pour pouvoir travailler dessus

#Pour sauvegarder la dataframe

df_complete.to_csv ('df_warehouses_and_clients_example.csv' , index = False)
#pour inverser l'opération : df_complete= pd.read_csv('df_warehouses_and_clients_example.csv')


#Pour sauvegarder le tableau des temps de trajets

np.savetxt("travel_times_array_example.csv", tableau_, delimiter=",")
#pour inverser l'opération : np.genfromtxt("travel_times_array_example.csv", delimiter=',')

#Pour sauvegarder le dictionnaire des itinéraires

with open('itineraries_dict_example.csv', 'w') as f:  
    w = csv.DictWriter(f, itineraires_.keys())
    w.writeheader()
    w.writerow(itineraires_)

"""Pour inverser l'opération : 
df_example = pd.read_csv('itineraries_dict_example.csv', header=None)
dict_example = {}
for i in range(df_example.shape[1]) :
    dict_example[df_example[i][0]] = df_example[i][1]

Note : il y a des guillemets autour des tuples lorsqu'on inverse l'opération"""

#Pour sauvegarder la liste des coordonées des points

"""Elle se déduit de la dataframe !!
coord_example = list(zip(list(df_complete['y']), list(df_complete['x'])))"""

from graphe_copy import *

g = Garage (2.2728354, 48.8281142997349, 40, 60)
c = Camion(50, 0, 10000)

k = 4 # choose number of clients
df, indexes, warehouses, parcels = create_graph_components(k)

G = Graph(g, warehouses, parcels, c)
G.make_graph()
G.make_dist_matrix(df)

G.matrix

generate_csv(G, df, indexes)

print(G.matrix)

coords, dist_matrix, itineraries_dict = itineraries(df, G_idf, "length")
carte_test = ox.folium.plot_route_folium(G_idf, itineraries_dict[(0, 1)][0], 
                                         tiles='Stamen Toner')

G_test = ox.graph_from_address("Paris", dist = 15000, simplify=True, network_type="drive")
ox.folium.plot_graph_folium(G_test)


### Test fonction itineraries



depart, arrivee = 1301278595, 499119053

start_time = time.time()
longueur, route = nx.bidirectional_dijkstra(G_idf, depart, arrivee, weight='corrected_travel_time')
print("temps :", time.time() - start_time, "secondes")

from graphe import *

g = Garage (2.2728354, 48.8281142997349, 40, 60)
c = Camion(50, 0, 10000)

k = 4 # choose number of clients
df, indexes, warehouses, parcels = create_graph_components(k)

G = Graph(g, warehouses, parcels, c)
G.make_graph()
G.make_dist_matrix(df)

generate_csv(G, df, indexes)

G.matrix
G.itineraries

from optim_gen_copy import *

with open('./output_data/other_data/itineraries_dict.csv', 'w') as f:  
    w = csv.DictWriter(f, G.itineraries.keys())
    w.writeheader()
    w.writerow(G.itineraries)

file_properties = generate_csv(G, df, indexes)
vehicle_capacity= file_properties.pop()
file_properties = no_client_to_deliver(file_properties)
file_properties = one_client_to_deliver(file_properties)
trucks = file_properties[1::3]
number_clients_per_warehouse = file_properties[2::3]
instances = [] #listes pour regrouper les résultats par entrepot
liste_res =[]
for (i, file) in enumerate(file_properties[::3]):
    instance = pd.read_csv(os.path.join(PATH, 'input_data', file))
    if instance.shape[0]>2 :
        instances += [instance]
    print(instance.head())
    max_vehicle = trucks[i]
    instance_bis = instance.drop(['Unnamed: 0', 'Identifiant', 'latitude', 'longitude'], axis = 'columns')
    n = instance_bis.shape[1]
    number_of_points = n - 1
    number_of_clients = number_clients_per_warehouse[i]
    instance_bis.columns = ['demand'] + [i for i in range(number_of_points)]
    distance_matrix = instance_bis[[i for i in range(0,number_of_points)]] #prend la matrice des colonnes
    res = run_vrptw(instance_bis, distance_matrix, vehicle_capacity, max_vehicle, number_of_clients, 100, 0.4, 0.2, 200)
    liste_res.append(res)

decode_to_GPS(liste_res, instances)


from graphe import *
from optim_gen_copy import simulation_vrptw
g = Garage (2.2728354, 48.8281142997349, 40, 60)
c = Camion(1, 0, 10000)

k = 5 # choose number of clients
simulation_vrptw(g, c, k)

import osmnx as ox

start_time = time.time()
route1 = nx.shortest_path(G_idf, 288357015, 4280286175, 'corrected_travel_time')
print("temps :", time.time() - start_time, "secondes")
    
start_time = time.time()
route2 = nx.dijkstra_path(G_idf, 288357015, 4280286175, 'corrected_travel_time')
print("temps :", time.time() - start_time, "secondes")

try : 
    import pillow
    a =  12
except ModuleNotFoundError :
    print("t'as pas ça sur ton ordi wesh")
    a = 13
print(a)
