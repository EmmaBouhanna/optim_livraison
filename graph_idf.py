import pandas as pd
import osmnx as ox
import networkx as nx
import csv
import geopandas

# Graph of Ile-de-France
G_idf_0 = ox.graph_from_place('Ile-de-France, France', network_type='drive', simplify=True)

# Adding speeds and travel times to the graph's edges
ox.speed.add_edge_speeds(G_idf_0)
ox.speed.add_edge_travel_times(G_idf_0)

# Converting the graph into geodataframes
gdf_nodes, gdf_edges = ox.graph_to_gdfs(G_idf_0)

# Converting the geodataframes into csv files (in order to store the data)
gdf_nodes.to_csv("gdf_nodes_idf.csv")
gdf_edges.to_csv("gdf_edges_idf.csv")

# Creating a smaller version of gdf_edges (in order to use it on GitHub)
gdf_edges_simplified = gdf_edges.drop(labels=["highway","area","junction","bridge","access","tunnel","width","est_width", "ref", "maxspeed", "lanes", "service", "name"], axis=1)
gdf_edges_simplified.to_csv("gdf_edges_idf_simplified.csv")

ox.folium.plot_graph_folium(G_idf_0)