#Importations
import osmnx as ox
import networkx as nx
import numpy as np
import pandas as pd
import random
import folium

from warehouses_clients import G_idf
import warehouses_clients
import routes

df_1 = pd.read_csv("warehouses.csv", sep=";")

nearest_nodes(df_1)

df_all = random_clients(20)

itineraries(df_1)

centre_Paris = [48.861146, 2.345721]
my_map = folium.Map(location = centre_Paris, tiles='Stamen Toner', zoom_start = 9, control_scale=True)

my_map

for i in range(n) :
    folium.Circle(radius=100, location=Coord[i], color='crimson', 
    fill=False).add_child(folium.Popup(f'{i}', show = False)).add_to(my_map)            

gdf_edges_idf

df_complete = random_clients(30)[0]

coord, tableau, itineraires = itineraries(df_complete, critere_optim="travel_time")

nearest_nodes(df)

ox.plot_graph(G_car)