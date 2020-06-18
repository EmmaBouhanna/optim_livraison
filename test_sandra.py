#Importations
import osmnx as ox
import networkx as nx
import numpy as np
import pandas as pd
import random
import folium

from routes import nearest_nodes
from warehouses_and_clients import random_clients
from warehouses_and_clients import G_idf, n_nodes, gdf_nodes_idf, gdf_edges_idf

df = pd.read_csv("warehouses.csv", sep=";")

Coord, Nodes = nearest_nodes(df)
n = df.shape[0]

centre_Paris = [48.861146, 2.345721]
my_map = folium.Map(location = centre_Paris, tiles='Stamen Toner', zoom_start = 9, control_scale=True)

my_map

for i in range(n) :
    folium.Circle(radius=100, location=Coord[i], color='crimson', 
    fill=False).add_child(folium.Popup(f'{i}', show = False)).add_to(my_map)            

gdf_edges_idf