
import osmnx as ox
import networkx as nx
import numpy as np
import pandas as pd
import random

#Création du graphe osmnx de l'Ile-de-France
G_idf = ox.graph_from_place('Ile-de-France, France', network_type='drive', simplify=True)

def nearest_nodes(df, G = G_idf):

    """
    Fonction qui détermine pour chacun des points le noeud osm le plus proche
    
    La fonction prend en argument:
    - df = une dataframe pandas contenant les points géographiques qu'on 
    cherche à relier et au moins les colonnes "Lon" (longitudes) et "Lat" (latitudes)
    - G : le graphe osmnx de la région géographique sur laquelle on travaille. Par défaut,
    G est le graphe du réseau routier d'Ile-de-France
    
    La fonction retourne :
    - Coord : la liste des tuples (latitude, longitude) pour chacun des points
    - Nearest_nodes : la liste des noeuds les plus proches
    """

    n = df.shape[0]
    Coord = list(zip(list(df["Lat"]), list(df["Lon"])))
    print(Coord)
    Nearest_nodes = [ox.distance.get_nearest_node(G, Coord[i]) for i in range(n)]
    return Coord, Nearest_nodes



def itineraries(df, G = G_idf, critere_optim = 'length'):

    """
    Fonction qui détermine pour chaque paire de points géographiques de la
    dataframe 
    
    La fonction prend en argument :
    - df = une dataframe pandas contenant les points géographiques qu'on 
    cherche à relier et au moins les colonnes "Lon" (longitudes) et "Lat" (latitudes)
    - G : le graphe osmnx de la région géographique sur laquelle on travaille. Par défaut,
    G est le graphe du réseau routier d'Ile-de-France
    - critere : chaîne de caractère, indique le critère à optimiser pour trouver les 
    meilleurs itineraires. Par défaut, on cherche les itinéraires les plus courts
    ("length"), mais on peut aussi chercher les itinéraires les plus rapides ("travel_time")

    La fonction retourne :
    - Tableau_distances : un tableau numpy dans lequel la case [i, j] contient la distance 
    de l’itinéraire le plus court allant de i à j (tableau pas forcément symétrique car 
    certaines routes peuvent êtres à sens unique)
    - Itineraires : un dictionnaire qui contient les routes :
        -> clé : (indice du départ, indice de l’arrivée)
        -> valeur : (route sous forme de liste de osm nodes, distance de cette route)
    """

    n = df.shape[0]

    Tableau_distances = np.zeros((n, n))
    Itineraires = {}

    Nearest_nodes = nearest_nodes(df, G)[1]

    for i in range(n) :
        depart = Nearest_nodes[i]
        for j in range(n):
            arrivee = Nearest_nodes[j]
            route = nx.shortest_path(G, depart, arrivee, weight=critere_optim)
            distance = int(sum(ox.utils_graph.get_route_edge_attributes(G, route, 'length')))
            Itineraires[(i, j)] = route, distance
            Tableau_distances[i, j] = distance

    return Tableau_distances, Itineraires 
