import pandas as pd
import osmnx as ox
import networkx as nx
import csv
import geopandas

#Création du graphe osmnx de l'Ile-de-France (fait une seule fois)

G_idf = ox.graph_from_place('Ile-de-France, France', network_type='drive', simplify=True)

gdf_nodes_idf, gdf_edges_idf = ox.graph_to_gdfs(G_idf)
gdf_nodes_idf = gdf_nodes_idf.rename(columns = {'x':'Lon'}) 
gdf_nodes_idf = gdf_nodes_idf.rename(columns = {'y':'Lat'})

gdf_nodes_idf.to_csv("gdf_nodes_idf.csv")
gdf_edges_idf.to_csv("gdf_edges_idf.csv")