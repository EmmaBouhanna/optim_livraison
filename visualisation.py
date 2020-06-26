
import os
import folium
from routes_improved import *

Paris_center = [48.861146, 2.345721]


def random_color():
    levels = range(32,256,32)
    return f"rgb{tuple(random.choice(levels) for _ in range(3))}"


def visualize_nearest_nodes(df, df_nodes = df_nodes_idf, my_map = None) :

    n = df.shape[0]

    coords_list, nearest_nodes_list = nearest_nodes(df)

    my_map = folium.Map(location = Paris_center, 
                    tiles='Stamen Toner', zoom_start = 9, control_scale=True)
    
    for i in range(n):

        folium.Circle(radius=100, location=coords_list[i], color='red',
                  fill=False).add_child(folium.Popup(f'{i}', show = True)).add_to(my_map)

        folium.Circle(radius=100, 
                  location=(df_nodes["y"][nearest_nodes_list[i]], df_nodes["x"][nearest_nodes_list[i]]), 
                  color='blue',
                  fill=False).add_child(folium.Popup(f'noeud {i}', show = True)).add_to(my_map)
    
    return my_map


files_list = []
for (root, dirs, files) in os.walk('./output_data'):
    files_list.extend(files)

def visualize_single_truck_travel():