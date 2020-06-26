
import os
import folium
from routes import *

Paris_center = [48.861146, 2.345721]

Lats = nx.get_node_attributes(G_idf, "y")
Lons = nx.get_node_attributes(G_idf, "x")


def random_color():
    levels = range(32,256,32)
    return f"rgb{tuple(random.choice(levels) for _ in range(3))}"


def visualize_nearest_nodes(df, my_map = None) :

    """Display on a map all geographical points of a dataframe and their respective
    nearest osm nodes.

    Input:
    - df (pandas.DataFrame) : dataframe 
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


# Create list containing "res_entrepot_i" files
files_list = []
for (root, dirs, files) in os.walk('./output_data'):
    files_list.extend(files)

if '.DS_Store' in files_list :
    files_list.remove('.DS_Store')



def visualize_single_truck_travel(stops_list, my_map=None):


