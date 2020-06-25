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

from graphe_sans_osmnx import *

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


