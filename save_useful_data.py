import pandas as pd
import osmnx as ox
import networkx as nx
import csv
import geopandas

from routes import *

""" 
STEP ZERO : saving useful data to gain some time
(see notebook 'Document complémentaire - améliorations du programme' for further detail) 
"""


#### ----------------------------- Graph of Ile-de-France -----------------------------

# Create graph of Ile-de-France
G_idf_0 = ox.graph_from_place('Ile-de-France, France', network_type='drive', simplify=True)

# Save the graph in gpickle format
nx.write_gpickle(G_idf_0, "./saved_files/graph_idf_simple.gpickle")

# Add speeds and travel times to the graph's edges
ox.speed.add_edge_speeds(G_idf_0)
ox.speed.add_edge_travel_times(G_idf_0)

# Save modified graph in gpickle format
nx.write_gpickle(G_idf_0, "./saved_files/graph_idf_speeds_travel_times.gpickle")

# Add corrected travel times 
# (see notebook 'Document complémentaire - améliorations du programme' for further detail) 
dict_ = {}
travel_times = nx.get_edge_attributes(G_idf_0, 'travel_time')
for key, value in travel_times.items():
    dict_[key] = value * 1.2

nx.set_edge_attributes(G_idf_0, dict_, 'corrected_travel_time')

# Save modified graph in pickle format
nx.write_gpickle(G_idf_0, "./saved_files/graph_idf_complete.gpickle")

# Converting the graph into geodataframes
gdf_nodes, gdf_edges = ox.utils_graph.graph_to_gdfs(G_idf_0)

# Converting the geodataframes into csv files (in order to store the data)
gdf_nodes.to_csv("./saved_files/gdf_nodes_idf.csv")
gdf_edges.to_csv("./saved_files/gdf_edges_idf.csv")

"""
# Creating a smaller version of gdf_edges (in order to use it on GitHub)
gdf_edges_simplified = gdf_edges.drop(labels=["highway","area","junction","bridge","access","tunnel","width","est_width", "ref", "maxspeed", "lanes", "service", "name"], axis=1)
gdf_edges_simplified.to_csv("gdf_edges_idf_simplified.csv")
"""



#### --------------------------------- Graph of Paris ---------------------------------

# Create graph of Ile-de-France
G_paris_0 = ox.graph_from_place('Paris, France', network_type='drive', simplify=True)

# Add speeds and travel times to the graph's edges
ox.speed.add_edge_speeds(G_paris_0)
ox.speed.add_edge_travel_times(G_paris_0)

# Add corrected travel times
dict_2 = {}
travel_times = nx.get_edge_attributes(G_paris_0, 'travel_time')
for key, value in travel_times.items():
    dict_2[key] = value * 1.2

nx.set_edge_attributes(G_paris_0, dict_2, 'corrected_travel_time')

# Save modified graph in gpickle format
nx.write_gpickle(G_paris_0, "./saved_files/graph_paris_complete.gpickle")

# Converting the graph into geodataframes
gdf_nodes_paris, gdf_edges_paris = ox.utils_graph.graph_to_gdfs(G_paris_0)

# Converting the geodataframes into csv files (in order to store the data)
gdf_nodes_paris.to_csv("./saved_files/gdf_nodes_paris.csv")
gdf_edges_paris.to_csv("./saved_files/gdf_edges_paris.csv")


#### ------------------------------------ Save data of warehouses ------------------------------------

coords_temps, tableau_temps, itineraires_temps = itineraries(df_warehouses, critere_optim="travel_time")
coords_temps_corrige, tableau_temps_corrige, itineraires_temps_corrige = itineraries(df_warehouses, critere_optim="corrected_travel_time")
coords_dist, tableau_dist, itineraires_dist = itineraries(df_warehouses, critere_optim="length")

# Save weight matrix for different weights
np.savetxt("./saved_files/travel_times_array_warehouses.csv", tableau_temps, delimiter=",")
np.savetxt("./saved_files/corrected_travel_times_array_warehouses.csv", tableau_temps_corrige, delimiter=",")
np.savetxt("./saved_files/lengths_array_warehouses.csv", tableau_dist, delimiter=",")

# Save itineraries dict for different weights

with open('./saved_files/travel_times_itineraries_warehouses.csv', 'w') as f:  
    w = csv.DictWriter(f, itineraires_temps.keys())
    w.writeheader()
    w.writerow(itineraires_temps)

with open('./saved_files/corrected_travel_times_itineraries_warehouses.csv', 'w') as f:  
    w = csv.DictWriter(f, itineraires_temps_corrige.keys())
    w.writeheader()
    w.writerow(itineraires_temps_corrige)

with open('./saved_files/lengths_itineraries_warehouses.csv', 'w') as f:  
    w = csv.DictWriter(f, itineraires_dist.keys())
    w.writeheader()
    w.writerow(itineraires_dist)