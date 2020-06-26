import os
import folium
import pandas as pd
from routes import *

Paris_center = [48.861146, 2.345721]

Lats = nx.get_node_attributes(G_idf, "y")
Lons = nx.get_node_attributes(G_idf, "x")

# Create list containing "res_entrepot_i" files
files_list = []
for (root, dirs, files) in os.walk('./output_data'):
    files_list.extend(files)

if '.DS_Store' in files_list :
    files_list.remove('.DS_Store')


# Load dict containing all-pairs itineraries (bricolage ici, à corriger)

df_itineraries = pd.read_csv('./output_data_bis/itineraries_dict.csv', header=None)
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



def random_color():
    levels = range(32,256,32)
    return f"rgb{tuple(random.choice(levels) for _ in range(3))}"



def visualize_nearest_nodes(df, my_map = None) :

    """Display on a map all geographical points of a dataframe and their respective
    nearest osm nodes.

    Input:
    - df (pandas.DataFrame) : dataframe 
    - my_map (folium.Map, optional) :
    """

    n = df.shape[0]

    coords_list, nearest_nodes_list = nearest_nodes(df)

    # Create a folium map if no map in input
    if my_map is None :
        my_map = folium.Map(location = Paris_center, 
                    tiles='Stamen Toner', zoom_start = 9, control_scale=True)
    
    for i in range(n):

        folium.Circle(radius=100, location=coords_list[i], color='red',
                  fill=False).add_child(folium.Popup(f'{i}', show = True)).add_to(my_map)

        folium.Circle(radius=100, 
                  location=(Lats[nearest_nodes_list[i]], Lons[nearest_nodes_list[i]]), 
                  color='blue',
                  fill=False).add_child(folium.Popup(f'noeud {i}', show = True)).add_to(my_map)
    
    return my_map



def visualize_single_truck_travel(stops_list, line_color='red' ,my_map=None):
    
    

