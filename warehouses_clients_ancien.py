import osmnx as ox
#import networkx as nx
import numpy as np
import pandas as pd
import random
import geopandas


#Version sans networkx

# Loading graph of Ile-de-France

df_nodes = pd.read_csv("gdf_nodes_idf.csv", index_col="osmid", dtype = {'osmid': int, 'y': float, 'x': float})
df_edges = pd.read_csv("gdf_edges_idf_simplified.csv")
df_nodes.drop(labels = "Unnamed: 0", axis = 1, inplace = True)
df_edges.drop(labels = "Unnamed: 0", axis = 1, inplace = True)

gdf_nodes = geopandas.GeoDataFrame(df_nodes)
gdf_edges = geopandas.GeoDataFrame(df_edges)

G_idf = ox.utils_graph.graph_from_gdfs(gdf_nodes, gdf_edges)


# Warehouses

df_warehouses = pd.read_csv("warehouses.csv", sep=";")

# Random clients

def random_clients(k, df = df_warehouses, G = G_idf) :

     """
    Add a number of random geographical points (representing random clients in our project) in a given area 
    to an existing dataframe (containing warehouses in our project)
    (Not inplace)

    Input:
    - k (int) : desired number of random clients
    - df (pandas.DataFrame) : dataframe containing following columns :
        - "y" : type float (latitudes)
        - "x" : type float (longitudes) 
        - "name" : type string
        - "type" : type string
        - "adress" : type string 
    - G (networkx.MultiDiGraph): graph of the given area
    

    Output :
    - df_complete (pandas.DataFrame) : output dataframe 
    - indexes (tuple) : tuple containing :
        - index_warehouses (list) : list containing start and end indexes of warehouses in df_complete
        - index_clients (list) : list containing start and end indexes of clients in df_complete
    """

    n_warehouses = df.shape[0]
    index_warehouses = [0, n_warehouses - 1]

    df_complete = df.copy()
    number_of_nodes = len(list(G_idf))
    Random_index = []

    for i in range(k):
        random_index = random.randint(0, number_of_nodes)
        while random_index in Random_index :
            random_index = random.randint(0, number_of_nodes)
        Random_index.append(random_index)
        random_node = list(G)[random_index]
        lat = gdf_nodes["y"][random_node]
        lon = gdf_nodes["x"][random_node]
        df_complete.loc[n_warehouses + i] = [lat, lon, f"Client {i}", None, None]
        
    index_clients = [n_warehouses, df_complete.shape[0] - 1]
    indexes = (index_warehouses, index_clients)

    return df_complete, indexes
