import numpy as np
import pandas as pd
import random
import osmnx as ox
import networkx as nx
from routes import G_idf 

gdf_nodes_idf, gdf_edges_idf = ox.graph_to_gdfs(G_idf)
gdf_nodes_idf = gdf_nodes_idf.rename(columns = {'x':'Lon'}) 
gdf_nodes_idf = gdf_nodes_idf.rename(columns = {'y':'Lat'})

n_nodes = nx.number_of_nodes(G_idf)

df_warehouses = pd.read_csv("warehouses.csv", sep=";")

def random_clients(k, df = df_warehouses) :

    """
    Fonction qui ajoute à une dataframe de points géographiques un certain nombre de points
    géographiques représentant des clients

    La fonction prend en entrée :
    - k : le nombre de clients qu'on veut générer aléatoirement
    - df : une dataframe de points géographiques (par exemple le garage et les entrepôts)
    Cette dataframe doit contenir des colonnes "Lat" et "Lon"
    

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
        random_node = list(nx.nodes(G_idf))[random.randint(0, m)]
        while node in Random_nodes :
            random_node = list(nx.nodes(G_idf))[random.randint(0, m)]
        lat = gdf_nodes_idf["Lat"][random_node]
        lon = gdf_nodes_idf["Lon"][random_node]
        df_complete.loc[n_warehouses + i] = [lat, lon, f"Client {i}", None, None]
        Random_nodes.append(random_node)
    
    index_clients = [n_warehouses, df_complete.shape[0] - 1]

    return df_complete, (index_warehouses, index_clients)