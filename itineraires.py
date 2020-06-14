import osmnx as ox
import networkx as nx
import numpy as np
import pandas as pd

G_idf = ox.graph_from_place('Ile-de-France, France', network_type='drive', simplify=True)

def nearest_nodes(G, df_points):

    """Fonction qui détermine pour chacun des points le noeud osm le plus proche
    
    La fonction prend en argument:
    - G : le graphe osmnx de la région géographique sur laquelle on travaille
    - df_points = une dataframe pandas contenant les points géographiques qu'on 
    cherche à relier et au moins les colonnes "Lon" (longitudes) et "Lat" (latitudes)
    
    La fonction retourne :
    - Coord : la liste des tuples (latitude, longitude) pour chacun des points
    - Nearest_nodes : la liste des noeuds les plus proches"""

    n = df_points.shape[0]

    Coord = []
    for i in range(n) :
        Coord.append((df["Lat"][i], df["Lon"][i]))

    Nearest_nodes = [ox.distance.get_nearest_node(G, Coord[i]) for i in range(n)]

    return Coord, Nearest_nodes



def itineraires(G, df_points, critere_optim = 'length'):

    """Fonction qui détermine pour chaque paire de points géographiques de la
    dataframe 
    
    La fonction prend en argument :
    - G : le graphe osmnx de la région géographique sur laquelle on travaille
    - df_points = une dataframe pandas contenant les points géographiques qu'on 
    cherche à relier et au moins les colonnes "Lon" (longitudes) et "Lat" (latitudes)
    - critere : chaîne de caractère, indique le critère à optimiser pour trouver les 
    meilleurs itineraires. Par défaut, on cherche les itinéraires les plus courts
    ("length"), mais on peut aussi chercher les itinéraires les plus rapides ("travel_time")

    La fonction retourne :
    - Tableau_distances
    - Itineraires
    """

    n = df_points.shape[0]

    Tableau_distances = np.zeros((n, n))
    Itineraires = {}

    Nearest_nodes = nearest_nodes(G, df_points)[1]

    for i in range(n) :
        depart = Nearest_nodes[i]
        for j in range(n):
            arrivee = Nearest_nodes[j]
            route = nx.shortest_path(G, depart, arrivee, weight=critere_optim)
            distance = int(sum(ox.utils_graph.get_route_edge_attributes(G, route, 'length')))
            Itineraires[(i, j)] = route, distance
            Tableau_distances[i, j] = distance

    return Tableau_distances, Itineraires 

