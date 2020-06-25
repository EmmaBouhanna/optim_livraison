import networkx as nx
import random
import pandas as pd


G_idf = nx.read_gpickle("./saved_files/graph_idf.gpickle")

df_nodes_idf = pd.read_csv("gdf_nodes_idf.csv", index_col="osmid", dtype = {'osmid': int, 'y': float, 'x': float})
df_edges_idf = pd.read_csv("gdf_edges_idf_simplified.csv")
df_nodes_idf.drop(labels = "Unnamed: 0", axis = 1, inplace = True)
df_edges_idf.drop(labels = "Unnamed: 0", axis = 1, inplace = True)

# Warehouses
df_warehouses = pd.read_csv("warehouses.csv", sep=";")

# Random clients

def random_clients(k, df = df_warehouses, G = G_idf, df_nodes = df_nodes_idf) :

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
    - df_nodes (pandas.DataFrame) : dataframe containing the nodes of G
    

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
        lat = df_nodes["y"][random_node]
        lon = df_nodes["x"][random_node]
        df_complete.loc[n_warehouses + i] = [lat, lon, f"Client {i}", None, None]
        
    index_clients = [n_warehouses, df_complete.shape[0] - 1]
    indexes = (index_warehouses, index_clients)

    return df_complete, indexes 