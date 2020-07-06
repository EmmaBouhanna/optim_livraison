import osmnx as ox
import numpy as np
import time
# networkx and pandas already imported in warehouses_clients

from warehouses_clients import *

"""
FIRST STEP : 

"""

def nearest_nodes(df, G=G_idf):
    """
    Find node nearest to each point of a dataframe. 

    Input :
    - df (pandas.DataFrame) : dataframe of geographical points. This dataframe must contain 
    at least the following columns :
        - "x" (longitudes)
        - "y" (latitudes)
    - G (networks.MultiDiGraph, optional): graph networkx of the area of interest. If not specified,
    G is the graph of Ile-de-France

    Output :
    - coords_list (list) : list containing tuples (latitude, longitude) for each node
    - nearest_nodes_list : list of osmid of the nearest nodes

    """

    n = df.shape[0]

    coords_list = list(zip(list(df['y']), list(df['x'])))
    nearest_nodes_list = [ox.distance.get_nearest_node(
        G, coords_list[i]) for i in range(n)]

    return coords_list, nearest_nodes_list


def itineraries(df, G=G_idf, critere_optim='corrected_travel_time'):
    """
    Find all-pairs best path (according to a given criteria)

    Input :
    - df (pandas.DataFrame) : dataframe of geographical points. This dataframe must contain 
    at least the following columns :
        - "x" (longitudes)
        - "y" (latitudes)
    - G (networks.MultiDiGraph, optional): graph networkx of the area of interest. If not specified,
    G is the graph of Ile-de-France
    - critere_optim (string, optional) : use this edge attribute as the edge weight that must be 
    minimized. If not specified, this attribute is 'corrected_travel_time'. Other supported options :
    'length', 'travel_time', ...

    Output :
    - coords_list (list) : list containing tuples (latitude, longitude) for each node
    - weight_array (numpy.ndarray) : un tableau numpy dans lequel la case [i, j] contient le "poids"
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

    if G == G_idf and critere_optim == 'corrected_travel_time':

        warehouses_array = np.genfromtxt(
            './saved_files/corrected_travel_times_array_warehouses.csv', delimiter=',')
        n_warehouses = np.shape(warehouses_array)[0]

        df_warehouses_itineraries = pd.read_csv(
            './saved_files/corrected_travel_times_itineraries_warehouses.csv', header=None)
        for i in range(df_warehouses_itineraries.shape[1]):
            itineraries_dict[df_warehouses_itineraries[i]
                             [0]] = df_warehouses_itineraries[i][1]

        some_values = True

    elif G == G_idf and critere_optim == 'travel_time':

        warehouses_array = np.genfromtxt(
            './saved_files/travel_times_array_warehouses.csv', delimiter=',')
        n_warehouses = np.shape(warehouses_array)[0]

        df_warehouses_itineraries = pd.read_csv(
            './saved_files/travel_times_itineraries_warehouses.csv', header=None)
        for i in range(df_warehouses_itineraries.shape[1]):
            itineraries_dict[df_warehouses_itineraries[i]
                             [0]] = df_warehouses_itineraries[i][1]

        some_values = True

    elif G == G_idf and critere_optim == 'length':

        warehouses_array = np.genfromtxt(
            './saved_files/lengths_array_warehouses.csv', delimiter=',')
        n_warehouses = np.shape(warehouses_array)[0]

        df_warehouses_itineraries = pd.read_csv(
            './saved_files/lengths_itineraries_warehouses.csv', header=None)
        for i in range(df_warehouses_itineraries.shape[1]):
            itineraries_dict[df_warehouses_itineraries[i]
                             [0]] = df_warehouses_itineraries[i][1]

        some_values = True

    coords_list, nearest_nodes_list = nearest_nodes(df, G)

    if some_values:  # weights already known for itineraries connecting warehouses
        start_time_ = time.time()
        for i in range(n):
            depart = nearest_nodes_list[i]
            for j in range(n):
                if (i < n_warehouses and j < n_warehouses):
                    # itinerary between two warehouses
                    weight_array[i, j] = warehouses_array[i, j]
                else:
                    arrivee = nearest_nodes_list[j]
                    route = nx.shortest_path(
                        G, depart, arrivee, weight=critere_optim)
                    total_weight = int(
                        sum(ox.utils_graph.get_route_edge_attributes(G, route, critere_optim)))
                    itineraries_dict[f'({i}, {j})'] = route, total_weight
                    weight_array[i, j] = total_weight
            print(
                f"Boucle {i} : temps d execution : {time.time() - start_time_} secondes ---")

    else:
        start_time_ = time.time()
        for i in range(n):
            depart = nearest_nodes_list[i]
            for j in range(n):
                arrivee = nearest_nodes_list[j]
                try:
                    route = nx.shortest_path(
                        G, depart, arrivee, weight=critere_optim)
                    total_weight = int(
                        sum(ox.utils_graph.get_route_edge_attributes(G, route, critere_optim)))
                    itineraries_dict[f'({i}, {j})'] = route, total_weight
                    weight_array[i, j] = total_weight
                except KeyError:
                    print(f'{critere_optim} is not a valid edge attribute, please create that edge attribute using function nx.set_edge_attributes or choose another edge attribute as critere_optim')
                    return None
            print(
                f"Boucle {i} : temps d execution : {time.time() - start_time_} secondes ---")

    print("Temps d execution total : %s secondes ---" %
          (time.time() - start_time))

    return coords_list, weight_array, itineraries_dict
