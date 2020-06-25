import osmnx as ox
import numpy as np
import time

# networkx and pandas already imported in warehouses_clients

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
    - coords_list : la liste des tuples (latitude, longitude) pour chacun des points
    - nearest_nodes_list : la liste des noeuds les plus proches
    """

    n = df.shape[0]

    coords_list = list(zip(list(df['y']), list(df['x'])))
    nearest_nodes_list = [ox.distance.get_nearest_node(G, coords_list[i]) for i in range(n)]
    
    return coords_list, nearest_nodes_list



def itineraries(df, G = G_idf, critere_optim = 'corrected_travel_time'):

    """
    Fonction qui détermine pour chaque paire de points géographiques de la
    dataframe 
    
    La fonction prend en argument :
    - df = une dataframe pandas contenant les points géographiques qu'on 
    cherche à relier et au moins les colonnes "x" (longitudes) et "y" (latitudes)
    - G : le graphe osmnx de la région géographique sur laquelle on travaille. Par défaut,
    G est le graphe du réseau routier d'Ile-de-France
    - critere : chaîne de caractère, indique le critère à optimiser pour trouver les 
    meilleurs itineraries_dict. Par défaut, on cherche les itinéraires les plus courts
    ("length"), mais on peut aussi chercher les itinéraires les plus rapides ("travel_time")

    La fonction retourne :
    - coords_list : la liste des tuples (latitude, longitude) pour chacun des points
    - weight_array : un tableau numpy dans lequel la case [i, j] contient le "poids"
    (distance ou temps de trajet par exemple)
    du meilleur itinéraire allant de i à j (tableau pas forcément symétrique car 
    certaines routes peuvent êtres à sens unique)
    - itineraries_dict : un dictionnaire qui contient les routes :
        -> clé (string) : '(indice du départ, indice de l’arrivée)'
        -> valeur (list) : route sous forme de liste de osm nodes, poids de cette route
    """

    # On mesure le temps d'exécution de la fonction
    start_time = time.time()

    n = df.shape[0]
    weight_array = np.zeros((n, n))
    itineraries_dict = {}
    some_values = False

    # On charge la matrice des poids et le dictionnaire des itinéraires relatifs aux entrepôts si ces données sont déjà sauvegardées

    if critere_optim == 'corrected_travel_time' :

        warehouses_array = np.genfromtxt('./saved_files/corrected_travel_times_array_warehouses.csv', delimiter=',')
        n_warehouses = np.shape(warehouses_array)[0]

        df_warehouses_itineraries = pd.read_csv('./saved_files/corrected_travel_times_itineraries_warehouses.csv', header=None)
        for i in range(df_warehouses_itineraries.shape[1]) :
            itineraries_dict[df_warehouses_itineraries[i][0]] = df_warehouses_itineraries[i][1]

        some_values = True

    elif critere_optim == 'travel_time' :

        warehouses_array = np.genfromtxt('./saved_files/travel_times_array_warehouses.csv', delimiter=',')
        n_warehouses = np.shape(warehouses_array)[0]
        
        df_warehouses_itineraries = pd.read_csv('./saved_files/travel_times_itineraries_warehouses.csv', header=None)
        for i in range(df_warehouses_itineraries.shape[1]) :
            itineraries_dict[df_warehouses_itineraries[i][0]] = df_warehouses_itineraries[i][1]
        
        some_values = True

    elif critere_optim == 'length' :

        warehouses_array = np.genfromtxt('./saved_files/lengths_array_warehouses.csv', delimiter=',')
        n_warehouses = np.shape(warehouses_array)[0]

        df_warehouses_itineraries = pd.read_csv('./saved_files/lengths_itineraries_warehouses.csv', header=None)
        for i in range(df_warehouses_itineraries.shape[1]) :
            itineraries_dict[df_warehouses_itineraries[i][0]] = df_warehouses_itineraries[i][1]
        
        some_values = True
    
    # rajouter une sécurité pour lever les erreurs (critere inexistant)

    coords_list, nearest_nodes_list = nearest_nodes(df, G)

    if some_values : # weights already known for itineraries connecting warehouses
        for i in range(n) :
            print("boucle", i)
            print("Temps d execution : %s secondes ---" % (time.time() - start_time))
            depart = nearest_nodes_list[i]
            for j in range(n):
                if (i < n_warehouses and j < n_warehouses):
                    # itinerary between two warehouses
                    weight_array[i, j] = warehouses_array[i, j]
                    print("value already calculated")
                else : 
                    arrivee = nearest_nodes_list[j]
                    route = nx.shortest_path(G, depart, arrivee, weight=critere_optim)
                    total_weight = int(sum(ox.utils_graph.get_route_edge_attributes(G, route, critere_optim)))
                    itineraries_dict[f'({i}, {j})'] = route, total_weight
                    weight_array[i, j] = total_weight
                    print("new value")
        print("Temps d execution total : %s secondes ---" % (time.time() - start_time))

    else :
        for i in range(n) :
            print("boucle", i)
            print("Temps d execution : %s secondes ---" % (time.time() - start_time))
            depart = nearest_nodes_list[i]
            for j in range(n):
                arrivee = nearest_nodes_list[j]
                route = nx.shortest_path(G, depart, arrivee, weight=critere_optim)
                total_weight = int(sum(ox.utils_graph.get_route_edge_attributes(G, route, critere_optim)))
                itineraries_dict[f'({i}, {j})'] = route, total_weight
                weight_array[i, j] = total_weight
        print("Temps d execution total : %s secondes ---" % (time.time() - start_time))
    
    return coords_list, weight_array, itineraries_dict
