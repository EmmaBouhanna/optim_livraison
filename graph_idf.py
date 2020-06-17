import pandas as pd
import osmnx as ox
import networkx as nx

#Création du graphe osmnx de l'Ile-de-France
G_idf = ox.graph_from_place('Ile-de-France, France', network_type='drive', simplify=True)

gdf_nodes_idf, gdf_edges_idf = ox.graph_to_gdfs(G_idf)
gdf_nodes_idf = gdf_nodes_idf.rename(columns = {'x':'Lon'}) 
gdf_nodes_idf = gdf_nodes_idf.rename(columns = {'y':'Lat'})

n_nodes = nx.number_of_nodes(G_idf)