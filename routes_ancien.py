
import osmnx as ox
import networkx as nx
import numpy as np
import pandas as pd
import time

from warehouses_clients import *


def nearest_nodes(df, G = G_idf):

    """
    Fonction qui détermine pour chacun des points le noeud osm le plus proche
    
    La fonction prend en argument:
    - df = une dataframe pandas contenant les points géographiques qu'on 
    cherche à relier et au moins les colonnes "x" (longitudes) et "y" (latitudes)
    - G : le graphe osmnx de la région géographique sur laquelle on travaille. Par défaut,
    G est le graphe du réseau routier d'Ile-de-France
    
    La fonction retourne :
    - Coord : la liste des tuples (latitude, longitude) pour chacun des points
    - Nearest_nodes : la liste des noeuds les plus proches
    """

    n = df.shape[0]

    Coord = list(zip(list(df['y']), list(df['x'])))
    Nearest_nodes = [ox.distance.get_nearest_node(G, Coord[i]) for i in range(n)]
    
    return Coord, Nearest_nodes



def itineraries(df, G = G_idf, critere_optim = 'length'):

    """
    Fonction qui détermine pour chaque paire de points géographiques de la
    dataframe 
    
    La fonction prend en argument :
    - df = une dataframe pandas contenant les points géographiques qu'on 
    cherche à relier et au moins les colonnes "x" (longitudes) et "y" (latitudes)
    - G : le graphe osmnx de la région géographique sur laquelle on travaille. Par défaut,
    G est le graphe du réseau routier d'Ile-de-France
    - critere : chaîne de caractère, indique le critère à optimiser pour trouver les 
    meilleurs itineraires. Par défaut, on cherche les itinéraires les plus courts
    ("length"), mais on peut aussi chercher les itinéraires les plus rapides ("travel_time")

    La fonction retourne :
    - Coord : la liste des tuples (latitude, longitude) pour chacun des points
    - Tableau_distances : un tableau numpy dans lequel la case [i, j] contient la distance 
    de l’itinéraire le plus court allant de i à j (tableau pas forcément symétrique car 
    certaines routes peuvent êtres à sens unique)
    - Itineraires : un dictionnaire qui contient les routes :
        -> clé : (indice du départ, indice de l’arrivée)
        -> valeur : (route sous forme de liste de osm nodes, distance de cette route)
    """

    start_time = time.time()

    n = df.shape[0]

    Tableau_distances = np.zeros((n, n))
    Itineraires = {}

    Coord, Nearest_nodes = nearest_nodes(df, G)

    for i in range(n) :
        print("boucle", i)
        print("Temps d execution : %s secondes ---" % (time.time() - start_time))
        depart = Nearest_nodes[i]
        for j in range(n):
            arrivee = Nearest_nodes[j]
            route = nx.shortest_path(G, depart, arrivee, weight=critere_optim)
            total_weight = int(sum(ox.utils_graph.get_route_edge_attributes(G, route, critere_optim)))
            Itineraires[i, j] = route, total_weight
            Tableau_distances[i, j] = total_weight
    print("Temps d execution total : %s secondes ---" % (time.time() - start_time))
    return Coord, Tableau_distances, Itineraires
