import osmnx as ox
import networkx as nx
import numpy as np
import pandas as pd
import random
import geopandas

# Graph of Ile-de-France

df_nodes = pd.read_csv("gdf_nodes_idf.csv")
df_edges = pd.read_csv("gdf_edges_idf_simplified.csv")
df_nodes.drop(labels = "Unnamed: 0", axis = 1, inplace = True)
df_edges.drop(labels = "Unnamed: 0", axis = 1, inplace = True)

gdf_nodes = geopandas.GeoDataFrame(df_nodes)
gdf_edges = geopandas.GeoDataFrame(df_edges)

G_idf = ox.utils_graph.graph_from_gdfs(gdf_nodes, gdf_edges)

number_of_nodes = df_nodes.shape[0]


# Warehouses

df_warehouses = pd.read_csv("warehouses.csv", sep=";")

# Random clients

def random_clients(k, df = df_warehouses, G = G_idf) :

    """
    Fonction qui ajoute à une dataframe de points géographiques un certain nombre de points
    géographiques représentant des clients

    La fonction prend en entrée :
    - k : le nombre de clients qu'on veut générer aléatoirement
    - df : une dataframe de points géographiques (par exemple le garage et les entrepôts)
    Cette dataframe doit contenir des colonnes "y"(latitudes) et "x"(longitudes)
    

    La fonction retourne :
    - df_complete : la dataframe complétée par les clients aléatoires 
    - indices : un doublet de listes d'indices :
    (indices des entrepôts, indices des clients)
    """

    n_warehouses = df.shape[0]
    index_warehouses = [0, n_warehouses - 1]

    df_complete = df.copy()
    Random_nodes = []

    for i in range(k):
        random_node = random.randint(0, df_nodes.shape[0])
        while random_node in Random_nodes :
            random_node = random.randint(0, df_nodes.shape[0])
        lat = gdf_nodes["y"][random_node]
        lon = gdf_nodes["x"][random_node]
        df_complete.loc[n_warehouses + i] = [lat, lon, f"Client {i}", None, None]
        Random_nodes.append(random_node)
    
    index_clients = [n_warehouses, df_complete.shape[0] - 1]

    return df_complete, (index_warehouses, index_clients)
