from __init__ import * 
#from warehouses_clients import *
#from routes import *


"""
SECOND STEP: Building a graph containing all the information about warehouses,
parcels and clients

This file contains all the classes and methods used to build the graph from 
the geographical locations of clients and warehouses obtained in the first step. 

NOTES : Lignes à modifier pour changer de fichiers :
fonction make_dist_matrix (ligne 288)
fonction create_graph_components (début - 2 premières lignes)


"""

class Node:
    """
    The class Node is the basic class for all nodes of the graph.
    Concretely, a node represents one geographical point in the city that 
    corresponds to a client, a warehouse ...
    Consquently, there will be different kinds of nodes (Entrepot, Client, Colis, Garage), 
    which will all inherit from Node.
    
    A Node is simply defined by its geograohical location: so by latitude and 
    longitude. 
    """
    
    def __init__(self, lat : float, long : float):
        """
        :param lat: latitude
        :type lat: float
        :param long: longitude
        :type long: float
        
        :attribute id: unique identifier generated thanks to the UIID python
        library
        :type id: uuid
        :attribute children: list of children nodes
        :type children: [Node]
        """
        self.id = uuid4()
        self.lat = lat
        self.long = long
        self.children = [] 
    
    
    def new_child(self, node):
        """
        Class method which adds a child to the children list when applied to a
        Node.
        
        :param node: child node to be added
        :type node: Node
        """
        self.children.append(node)
    
    def __eq__(self, node):
        """
        Redefinition of equality for nodes
        Two nodes are equal if they have the same identifier.
        
        :param node: node to be compared with
        :type node: Node
        
        :return: True if the nodes are equal, False if they aren't
        :rtype: boolean
        """
        if self.id == node.id:
            return True
        else:
            return False


class Client(Node): 
    """
    Subclass of Node representing clients.
    A client will (almost) always be created starting from a parcel. 
    This class is essentially used in the implementation of the graph's 
    visualization.
    """
    
    def __init__(self, lat : float, long : float, size = None):
        """
        Almost the same __init__ of the upper class: there is an additional attribute.
        
        :attribute taille_colis: size of a client's parcel
        :type taille_colis: int (if not None)
        """
        self.id = uuid4()
        self.lat = lat
        self.long = long
        self.taille_colis = size
        self.children = []
    
def make_client(lat : float, long : float, size: int):
    """
    Method to build a client.
    
    :param lat: latitude
    :type lat: float
    :param long: longitude
    :type long: float
    :param size: size of the client's parcel (in m^3)
    :type size: int
    
    :return: a new Client 
    :rtype: Client (Node) 
    """
    new_client = Client(lat, long, size)
    return new_client
    
    
class Colis(Node):
    """
    Subclass of Node representing parcels.
    Contrary to other nodes, it has no geographical coordinates as attributes
    since a parcel will travel from the warehouse up to a client.
    """
    
    def __init__(self, size: int, entrepot, destination):
        """
        __init__ builds an object with more attributes than the upper class.
        
        :param destination: coordinates of the client who bought the parcel
        :type destination: list of floats (lenght = 2)
        
        
        :attribut size: parcel's size (in m^3)
        :type size: int
        :attribute entrepot: warehouse where the parcel is stored
        :type entrepot: Entrepot (Node)
        :attribute client: client who bought the parcel
        :type client: Client (Node)
        """
        self.id = uuid4()
        self.size = size
        self.entrepot = entrepot
        self.client = make_client(destination[0], destination[1], size)
        self.children = []
        

class Garage(Node):
    """
    Subclass of Node representing a garage.
    """
    
    def __init__(self, lat: float, long: float, nb_camions: int, nb_legers: int):
        """
        :attribute nb_camions: maximum number of trucks in the garage
        :type nb_camions: int
        :attribute nb_legers: maximum number of light/small trucks in the garage
        :type nb_legers: int
        """
        self.id = uuid4()
        self.lat = lat
        self.long = long
        self.nb_camions = nb_camions
        self.nb_legers = nb_legers
        self.children = []

class Entrepot(Node):
    """
    Subclass of Node representing a warehouse.
    """
    
    def __init__(self, lat : float, long : float, max_camions : int, max_legers: int, capacite : int):
        """
        :attribute max_camions: maximum number of trucks
        :type max_camions: int
        :attribute max_legers: maximum number of light/small trucks
        :type max_legers: int
        :attribute capacite: storage capacity of the warehouse (in m^3)
        :type capacite: int
        """
        self.id = uuid4()
        self.lat = lat
        self.long = long
        self.children = []
        self.max_camions = max_camions
        self.max_legers = max_legers
        self.capacite = capacite



class Vehicule:
    """ 
    Generic class for all vehicles. 
    For the moment, our algorithm only optimizes the delivery network by using 
    trucks. Further developments can lead to use bycicles, smaller trucks...
    """
    def __init__(self, capacite, pollution, dist_max, temps, route_etroite : bool):
        """
        :attribute capacite: maximum load capacity of the vehicle (in m^3)
        :type capacite: int
        :attribute pollution: malus/bonus due to the high/low carbone emissions
        of the vehicle
        :type pollution: float
        :attribute dist_max: maximum distance that can be traveled with one 
        refueling
        :type dist_max: int
        :attribute temps: time of the driver
        :type temps: float
        :attribute route_etroite: True if the vehicle can go in narrow streets,
        False if not
        :type route_etroite: boolean
        """
        self.capacite = capacite
        self.pollution = pollution
        self.dist_max = dist_max
        self.route_etroite = route_etroite
        self.temps = temps 

class Camion(Vehicule):
    """
    Subclass of Vehicle representing trucks.
    """
    def __init__(self, capacite, pollution, dist_max, route_etroite = False):
        self.capacite = capacite
        self.pollution = pollution
        self.dist_max = dist_max
        self.route_etroite = route_etroite

class Graph:
    """
    Class representing a graph whose nodes are garages, warehouses and clients.
    
    Structure: there are 3 genrations in the graph:
    1. The garage is the root: its children are warehouses
    2. Warehouses: its children are clients
    3. Clients
    
    How to build the graph thanks to the data collected during the first step 
    (an example is given in the test file):
    1. call the function create_graph_components
    2. call the function make_graph
    3. if you want to see a schematic representation of the graph, call 
    trace_graph
    4. call generate_csv to transform the graph into a csv file to be used in 
    the third step
    """
    
    def __init__(self, garage, entrepots: [Entrepot], colis: [Colis], camion : [Camion]):
        """
        :attribute garage: the root
        :type garage: Garage (Node)
        :attribute entrepots: list of warehouses where the parcels are stored
        :type entrepots: list of Entrepot (Node)
        :attribute colis: list of all parcels to be delivered
        :type colis: list of Colis (Node)
        :attribute camion: list of trucks that will be used for the delivery
        :type camions: list of Camion (Vehicle)
        :attribute k: number of clients
        :type k: int
        """
        self.garage = garage #la racine 
        self.entrepots = entrepots # liste des entrepots (fixée)
        self.colis = colis # liste des colis à livrer le jour n
        self.camion = camion
        self.k = len(colis) # nombre de clients
        self.matrix = None # distance matrix that will be computed
        self.coords = None

        
    def make_graph(self):
        """
        Class method used to build the graph from its components. 
        
        We start from the root (garage) and we successively add the warehouses
        (garage's children) and the clients (warehouses's children).
        All clients whose parcels come from the same house are children to each
        other. Indeed we want to be able to go from any of them to another one
        in order to then determine the best itinerary.
        """
        for e in self.entrepots:
            self.garage.new_child(e) # edge oriented from the garage to the warehouse
            colis_e = [] # list of parcels stored in the warehouse e
            for p in self.colis:
                if p.entrepot == e:
                    colis_e.append(p)
            for p in colis_e:
                e.new_child(p.client) # edge oriented from the warehouse to the client
                for pp in colis_e:
                    if pp.id != p.id:
                        p.client.new_child(pp.client)
        
    def make_dist_matrix(self, df = None):
        if self.matrix == None:

            coords = list(zip(list(df['y']), list(df['x'])))
            dist_matrix = np.genfromtxt(os.path.join(PATH, "output_data_bis/corrected_travel_times_array.csv", delimiter=','))
            df_itineraries = pd.read_csv(os.path.join(PATH, "output_data_bis/itineraries_dict.csv", delimiter=','), header=None)
            itineraries_dict = {}
            for i in range(df_itineraries.shape[1]) :
                # partie suivante c'est du bricolage parce qu'on a sauvegardé le dictionnaire
                # et que toutes les valeurs sont devenues des chaînes de caractères
                cleaned_ = df_itineraries[i][1].split('[')[1]
                cleaned_ = cleaned_.split(']')[0]
                # à ce stade on a une chaîne de caractère qui contient tous les identifiants
                # des noeuds de la route
                route = cleaned_.split(', ')
                for j in range(len(route)) :
                    route[j] = int(route[j])
                # route est la liste des identifiants des noeuds de la route
                itineraries_dict[df_itineraries[i][0]] = route

            self.matrix = dist_matrix
            self.coords = coords
            self.itineraries = itineraries_dict

    
    
def generate_csv(G : Graph, df = None, indexes = None):
    """
    Class method used to generate csv files that are going to be used in 
    the third step (optimization of the delivery). One csv file is created
    for each warehouse thanks to the method csv_entrepot.
    The method also stores the number of trucks that leave the garage as 
    well as the number of clients to be delivered.
    
    :param df: dataframe to get the true distance
    :type df: pandas dataframe
    
    :return: a list containg the names of the csv files, the number of 
    trucks and the number of clients
    :rtype: list
    """
    numero = 0
    file_names = []
    for e in G.entrepots:
        csv_entrepot(e, numero, G, df, indexes)
        name = "entrepot_"+str(numero)+".csv"
        file_names.append(name)
        file_names.append(e.max_camions)
        file_names.append(len(e.children))
        numero += 1
    file_names.append(G.camion.capacite)
    return file_names
    

def csv_entrepot(e, numero: int, G : Graph, df = None, indexes = None):
    """
    This method creates, for the warehouse given as an argument, a csv file 
    contaning the following elements:
    1. columns: [dentifier, demand, latitude, longitude, warehouse, client_1, ..., 
    client_k]
    2. rows: [warehouse, client_1, ..., client_k]
    3. For i in [0, k] and j in [4, 4+k], the cell [i, j] gives the distance 
    to go from the node i to the node j
    
    :param e: warehouse
    :type e: Warehouse (Node)
    :param numero: number of the warehouse (used in generate_csv)
    :type numero: int
    :param df: dataframe to get the true distance
    :type df: pandas dataframe
    
    :return: csv file in the folder "input_data"
    """
    
    index_start_warehouses = indexes[0][0]
    index_end_warehouses = indexes[0][1]
    index_start_clients = indexes[1][0]
    index_end_clients = indexes[1][1]
    
    L = [] # L is a list of lists
    # First element of L corresponds to the warehouse's data
    # find the warehouse in df
    index = -1
    for i in range(index_start_warehouses, index_end_warehouses +1):
        if e.lat == df["y"][i] and e.long == df["x"][i]:
            index = i
           
    l = [index, 0, e.lat, e.long]
    tree_nodes = [e]+e.children
    for n in tree_nodes:
        l.append(dist(e, n, G))
    L.append(l)
    
    
    # All other elements of L correspond to the clients' data
    for client in e.children:
        # find the client in df
        index = -1
        for i in range(index_start_clients, index_end_clients +1):
            if client.lat == df["y"][i] and client.long == df["x"][i]:
                index = i
        l = [index, client.taille_colis, client.lat, client.long]
        for n in tree_nodes:
            l.append(dist(client, n, G)) # distance from the node client to the node n
        L.append(l)
    names = ["Identifiant", "Demande", "latitude", "longitude", "entrepot"]
    tree_nodes.pop(0)
    for i in range(len(e.children)):
        ch = "client "+ str(i+1)
        names.append(ch)
    df = pd.DataFrame(L, columns = names)
    name = "entrepot_"+str(numero)+".csv"
    csv = df.to_csv(os.path.join(PATH, 'input_data', name))
    return (csv)    
    


def create_graph_components(k: int):
    """
    Method that creates warehouses and parcels from the data collected in the
    first step.
    1. call random_clients to get the dataframe of all warehouses and k clients
    as well as the list of indexes (saying where warehouses/clients start/end 
    in the dataframe)
    2. create all warehouses
    3. create all parcels (and clients)
    
    :param k: number of parcels
    :type k: int
    
    :return: dataframe, warehouses and parcels
    :rtype: dataframe pandas, [Entrepot], [Colis]
    """
    
    df = pd.read_csv(os.path.join(PATH, 'output_data_bis/df_complete.csv'))
    indexes = ([0, 19], [20, df.shape[0] - 1])

    localisations = df.values.tolist()
    index_start_warehouses = indexes[0][0]
    index_end_warehouses = indexes[0][1] 
    index_start_clients = indexes[1][0]
    index_end_clients = indexes[1][1]
    
    # creation of warehouses
    warehouses = []
    for i in range(index_start_warehouses, index_end_warehouses + 1):
        lat, long = localisations[i][0], localisations[i][1]
        capacity = 400000 #m^3
        max_vehicles = 50
        max_light = 30
        warehouses.append(Entrepot(lat, long, max_vehicles, max_light, capacity))
    
    # creation of parcels
    w = len(warehouses) 
    parcels = []
    for i in range(index_start_clients, index_end_clients + 1):
        destination = [localisations[i][0], localisations[i][1]]
        # parcel's size is random
        size = 0.01*np.random.randint(1, 100) # parcel sizes range from 10 cm^3 to 1 m^3
        random_draw = np.random.randint(0, w)
        where_from = warehouses[random_draw] # MODIF ICI random_draw au lieu de w
        parcels.append(Colis(size, where_from, destination))
        
    return df, indexes, warehouses, parcels



            
    
def dist (n1: Node, n2: Node, G: Graph):
    """
    Method that returns the distance between two nodes.
    If the graph is built thanks to real data, the distance returned is the one
    corresponding to the itinerary between the two nodes. If not, it is the 
    euclidean distance.
    
    :param n1: first node
    :type n1: Node
    :param n2: second node
    :type n2: Node
    :param df: dataframe to get the true distance
    :type df: pandas dataframe
    
    :return: distance to go from n1 to n2 (oriented edge)
    :rtype: float
    """
    if G.coords == None: # for an example without using real data
        dist = np.sqrt((n1.lat -n2.lat)**2 + (n1.long -n2.long)**2)
        
    else:
        coords = G.coords
        dist_matrix = G.matrix
        
        if isinstance(n1, Garage):
            dist = 0 
        elif isinstance(n2, Garage):
            dist = 0
        else:
            for el in coords:
                if n1.lat == el[0] and n1.long == el[1]:
                    i = coords.index((n1.lat, n1.long))
                if n2.lat == el[0] and n2.long == el[1]:
                    j = coords.index((n2.lat, n2.long))
            dist = dist_matrix[i][j]
    
    return(dist)



''' Je commente ce passage parce que cela ne marche pas sur mon ordi'''
# def trace_graph(graph):
#     G = pgv.AGraph(directed = True)
#     root = graph.garage
#     #G.add_node(root)
#     file = [root]
#     while len(file) >0:
#         if isinstance(file[0], Garage):
#             G.add_node(file[0], color = "black")
#         if isinstance(file[0], Entrepot):
#             G.add_node(file[0], color = "blue")
#         if isinstance(file[0], Client):
#             G.add_node(file[0], color = "pink")
#         for c in file[0].children:
#             if len(c.children)>0 and (file[0] in c.children):
#                 G.add_edge(file[0], c, color = "orange", label = str(round(dist(file[0], c), 1)))
#                 # G.add_edge(c, file[0], color = "orange")

#             if len(c.children) > 0 and (file[0] in c.children) == False:
#                 G.add_edge(file[0], c, color = "blue", label = str(round(dist(file[0], c), 1)))
#                 file.append(c)
#             if len(c.children) == 0:
#                 G.add_edge(file[0], c, color = "blue", label = str(round(dist(file[0], c), 1)))
#                 file.append(c)   
#         file.pop(0)
    
    # G.layout(prog='dot')
    # G.draw('file.png') 
    # a = Image.open('file.png')
    # a.show()
