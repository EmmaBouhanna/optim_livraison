from __init__ import *
from warehouses_and_clients import *
from routes import *

class Node:
    def __init__(self, lat : float, long : float):
        self.id = uuid4()
        self.lat = lat
        self.long = long
        self.children = []  # dico où les cles sont les identifiants, les valeurs [id,  et les valeurs le poids des aretes
    
    
    def new_child(self, node):  # crée un fils 
        # distance au père est la distance euclidienne
        self.children.append(node)
    
    def __eq__(self, node):
        if self.id == node.id:
            return True
        else:
            return False


class Client(Node): 
    def __init__(self, lat : float, long : float, size = None): # pour le moment 1 colis par client!!!
        self.id = uuid4()
        self.lat = lat
        self.long = long
        self.taille_colis = size
        self.children = []
    
def make_client(lat : float, long : float, size: int):
    new_client = Client(lat, long, size)
    return new_client
    
    
class Colis(Node):
    def __init__(self, size, entrepot: Node, destination):
        self.id = uuid4()
        self.size = size
        self.entrepot = entrepot
        self.client = make_client(destination[0], destination[1], size)
        self.children = []
        

class Garage(Node):
    def __init__(self, lat: float, long: float, nb_camions: int, nb_legers: int):
        self.id = uuid4()
        self.lat = lat
        self.long = long
        self.nb_camions = nb_camions
        self.nb_legers = nb_legers
        self.children = []

class Entrepot(Node):
    def __init__(self, lat : float, long : float, max_camions : int, max_legers: int, capacite : int):
        self.id = uuid4() # retrouver comment faire des identifiants uniques (avec un itérable?)
        self.lat = lat
        self.long = long
        self.children = []
        self.max_camions = max_camions
        self.max_legers = max_legers
        self.capacite = capacite



class Vehicule:
    def __init__(self, capacite, pollution, dist_max, temps, route_etroite : bool):
        self.capacite = capacite
        self.pollution = pollution
        self.dist_max = dist_max
        self.route_etroite = route_etroite
        self.temps = temps # temps du camioneur 

class Camion(Vehicule):
    def __init__(self, capacite, pollution, dist_max, route_etroite = False):
        self.capacite = capacite
        self.pollution = pollution
        self.dist_max = dist_max
        self.route_etroite = route_etroite
        
class Leger(Vehicule):
    def __init__(self, capacite, pollution = 0, dist_max = 10, route_etroite = True):
        self.capacite = capacite
        self.pollution = pollution
        self.dist_max = dist_max
        self.route_etroite = route_etroite    

class Graph:
    def __init__(self, garage, entrepots: [Entrepot], colis: [Colis], camion : [Camion]):
        self.garage = garage #la racine 
        self.entrepots = entrepots # liste des entrepots (fixée)
        self.colis = colis # liste des colis à livrer le jour n
        self.camion = camion
        self.k = len(colis) # nombre de clients


        
    def make_graph(self):
        # self.graph_list.append(self.garage)
        for e in self.entrepots:
            self.garage.new_child(e) # arete orientée du garage vers l'entrepot
            colis_e = [] # liste des paquets qui partent de e
            for p in self.colis:
                if p.entrepot == e:
                    colis_e.append(p)
            for p in colis_e:
                e.new_child(p.client) # arete orientée de l'entrepot vers le client
                for pp in colis_e:
                    if pp.id != p.id:
                        p.client.new_child(pp.client) # NB: pour le moment on "perd" le paquet dans la construction du graphe
        
    
    def generate_csv(self):
        numero = 1
        file_names = []
        
        # pour stocker le nombre de camions qui sortent du garage, ainsi que le nombre de clients à livrer
        for e in self.entrepots:
            csv_entrepot(e, numero)
            name = "entrepot_"+str(numero)+".csv"
            file_names.append(name)
            file_names.append(e.max_camions)
            file_names.append(len(e.children))
            numero += 1
        file_names.append(self.camion.capacite)
        return file_names
    
    


def create_graph_components(k: int):
    df, indexes = random_clients(k, df = df_warehouses)
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
        size = 0.01*np.random.randint(1, 100) # parcel sizes range from 10 cm^3 to 1 m^3
        random_draw = np.random.randint(0, w)
        where_from = warehouses[w] #COM SANDRA : w-1 plutot?
        parcels.append(Colis(size, where_from, destination))
        
    return df, warehouses, parcels

def dist (n1: Node, n2: Node, G:Graph, df):
    coords, dist_matrix, itineraries = itineraries(df, G = G_idf, critere_optim = 'length')
    
    if isinstance(n1, Garage):
        dist = 1234 # cout de Emma??
    elif isinstance(n2, Garage):
        dist = 1234
    else:
        for el in coords:
            if n1.lat == el[0] and n1.long == el[1]:
                i = coords.index((n1.lat, n1.long))
            if n2.lat == el[0] and n2.long == el[1]:
                j = coords.index((n1.lat, n1.long))
        dist = dist_matrix[i][j]
    return(dist)

def csv_entrepot(e, numero: int):
    # L est une liste de listes
    L = []
    # 1èr élément de la liste correspond aux données de l'entrepot
    l = [e.id, 0, e.lat, e.long]
    tree_nodes = [e]+e.children
    for n in tree_nodes:
        l.append(dist(e, n))
    L.append(l)
    # les autres éléments de L correspondent aux données des clients de l'entrepot
    for client in e.children:
        l = [client.id, client.taille_colis, client.lat, client.long]
        for n in tree_nodes:
            l.append(dist(client, n)) # convention: route du noeud client vers l'autre noeud
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
