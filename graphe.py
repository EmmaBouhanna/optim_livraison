import numpy as np
import pandas as pd
import csv
from uuid import uuid4
# import pygraphviz as pgv
# from PIL import Image

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
    
def dist(node1, node2):
        return np.sqrt((node1.lat - node2.lat)**2 +(node1.long - node2.long)**2)


class Client(Node): 
    def __init__(self, lat : float, long : float, size = None): # pour le moment 1 colis par client!!!
        self.id = uuid4()
        self.lat = lat
        self.long = long
        self.taille_colis = size
        self.children = []
        self.str = "client"
    
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
        self.str = "garage"

class Entrepot(Node):
    def __init__(self, lat : float, long : float, max_camions : int, max_legers : int, capacite : int):
        self.id = uuid4() # retrouver comment faire des identifiants uniques (avec un itérable?)
        self.lat = lat
        self.long = long
        self.children = []
        self.max_camions = max_camions
        self.max_legers = max_legers
        self.capacite = capacite
        self.str = "entrepot"

class Route: # j'aurais tendance à mettre ces infos (enfin etroite uniquement) dans le dico directement
    def __init__(self, vitesse, etroite : bool, dist):
        self.vitesse = vitesse # vitesse max autorisée en km/h
        self.etroite = etroite
        self.dist = dist


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
    def __init__(self, garage, entrepots: [Entrepot], points_relais: [Entrepot], colis: [Colis]):
        self.garage = garage #la racine 
        self.entrepots = entrepots # liste des entrepots (fixée)
        self.points_relais = points_relais
        self.colis = colis # liste des colis à livrer le jour n

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
        
        for r in self.points_relais:
            for p in self.colis:
                if dist(r, p) < 5: # périmètre de 5 km
                    r.new_child(p.client)
                    p.client.new_child(r)  
    
    
    def generate_csv(self, g):
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
        file_names.append(g.nb_camions) 
        return file_names

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
    csv = df.to_csv(name)
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
