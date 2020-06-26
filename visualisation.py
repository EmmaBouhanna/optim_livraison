import os
import folium
import pandas as pd
import osmnx as ox

from routes import *

Paris_center = [48.861146, 2.345721]

Lats = nx.get_node_attributes(G_idf, "y")
Lons = nx.get_node_attributes(G_idf, "x")

df_complete = pd.read_csv('./output_data_bis/df_complete.csv', usecols = ["y", "x", "name", "type", "adress"])

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



def visualize_nearest_nodes(df, input_map = None, n_warehouses=None) :

    """Display on a map all geographical points of a dataframe and their respective
    nearest osm nodes.

    Input:
    - df (pandas.DataFrame) : dataframe 
    - my_map (folium.Map, optional) :
    """

    n = df.shape[0]

    coords_list, nearest_nodes_list = nearest_nodes(df)

    # Create a folium map if no map in input
    if input_map is None :
        my_map = folium.Map(location = Paris_center, 
                    tiles='Stamen Toner', zoom_start = 9, control_scale=True)
    
    else :
        my_map = input_map

    if n_warehouses is None :
    
        for i in range(n):

            folium.Circle(radius=100, location=coords_list[i], color='red',
                    fill=False).add_child(folium.Popup(f'{i}', show = True)).add_to(my_map)

            folium.Circle(radius=100, 
                    location=(Lats[nearest_nodes_list[i]], Lons[nearest_nodes_list[i]]), 
                    color='blue',
                    fill=False).add_child(folium.Popup(f'noeud {i}', show = True)).add_to(my_map)

    else : 
        
        for i in range(n_warehouses):

            folium.Circle(radius=100, location=coords_list[i], color='red',
                    fill=False).add_child(folium.Popup(f'{i}', show = True)).add_to(my_map)

            folium.Circle(radius=100, 
                    location=(Lats[nearest_nodes_list[i]], Lons[nearest_nodes_list[i]]), 
                    color='orange',
                    fill=False).add_child(folium.Popup(f'noeud {i}', show = True)).add_to(my_map)
    
        for i in range(n_warehouses, n):

            folium.Circle(radius=100, location=coords_list[i], color='blue',
                    fill=False).add_child(folium.Popup(f'{i}', show = True)).add_to(my_map)

            folium.Circle(radius=100, 
                    location=(Lats[nearest_nodes_list[i]], Lons[nearest_nodes_list[i]]), 
                    color='green',
                    fill=False).add_child(folium.Popup(f'noeud {i}', show = True)).add_to(my_map)
        
    return my_map


def visualize_travel_between_two_nodes(start, end, line_color='red', input_map=None, G=G_idf):
    """
    Input :
    - start (int) : index (in the dataframe) of the start point 
    - end (int) : index (in the dataframe) of the start point 
    - line_color (str)
    - input_map (folium.Map)

    Output :
    - my_map (folium.Map)
    """

    if input_map is None :
        my_map = folium.Map(location = Paris_center,
                    tiles='Stamen Toner', zoom_start = 9, control_scale=True)
    
    else :
        my_map = input_map

    path = itineraries_dict[f'({start}, {end})']

    ox.folium.plot_route_folium(G, path, route_map=my_map, tiles='Stamen Toner', 
                            popup_attribute = "name",
                            route_color = line_color,
                            route_width=5, route_opacity=0.5)
   
    return my_map



def visualize_single_truck_travel(stops_list, color='red', input_map_=None, G=G_idf):

    """
    Input :
    - stops_list (list) : list of dataframe indexes of the nodes visited by the truck
    - line_color :
    - input_map
    _ G : graph used to calculate itineraries

    Output :

    """

    start = int(stops_list[0])
    end = int(stops_list[1])
    my_map = visualize_travel_between_two_nodes(start, end, line_color=color, input_map=input_map_)

    if len(stops_list) > 2 :

        for i in range(2, len(stops_list)):

            start = int(stops_list[i-1])
            end = int(stops_list[i])
            new_map = visualize_travel_between_two_nodes(start, end, line_color=color, input_map=my_map)
            my_map = new_map

    return my_map    


def visualize_single_truck_travel_2(stops_list, color='red', input_map=None, G=G_idf):

    #NE MARCHE PAS

    """
    Input :
    - stops_list (list) : list of dataframe indexes of the nodes visited by the truck
    - line_color :
    - input_map
    _ G : graph used to calculate itineraries

    Output :

    """

    if input_map is None :
        my_map = folium.Map(location = Paris_center,
                    tiles='Stamen Toner', zoom_start = 9, control_scale=True)
    
    else :
        my_map = input_map

    path = []

    for i in range(1, len(stops_list)):
        start = int(stops_list[i])
        end = int(stops_list[i-1])
        path += itineraries_dict[f'({start}, {end})']
        print(f"path : {path}")

    print(f"path : {path}")


    ox.folium.plot_route_folium(G, path, route_map=my_map, tiles='Stamen Toner', 
                            popup_attribute = "name",
                            route_color = color,
                            route_width=5, route_opacity=0.5)    

    return my_map    


def visualize_single_warehouse_travel(res_csv, preexisting_map=None, G=G_idf) :

    if preexisting_map is None :
        output_map = folium.Map(location = Paris_center,
                    tiles='Stamen Toner', zoom_start = 9, control_scale=True)
    else :
        output_map = preexisting_map        

    res_df = pd.read_csv(res_csv)
    if "Unnamed: 0" in list(res_df):
        res_df.drop(labels = "Unnamed: 0", axis = 1, inplace = True)

    trucks_list = list(res_df)

    # Display the location of the warehouse
    warehouse = int(res_df[trucks_list[0]][0])
    lat_w = df_complete["y"][warehouse]
    lon_w = df_complete["x"][warehouse]
    folium.Circle(radius=300, location=(lat_w, lon_w), color='red',
                    fill=True).add_child(folium.Popup(f'entrepot {warehouse}', show = True)).add_to(output_map)

    for truck in trucks_list :
        truck_color = random_color()
        stops_list = []
        for stop in list(res_df[truck]) :
            try :
                stops_list.append(int(stop))
            except ValueError :
                pass
        output_map = visualize_single_truck_travel(stops_list, color=truck_color, 
                                                    input_map_=output_map, G = G_idf)
    
    return output_map

"""

res_df = pd.read_csv('output_data/res_entrepot_6.csv')
res_df.drop(labels = "Unnamed: 0", axis = 1, inplace = True)

list(res_df["Camion 1"])

route1 = [1.0, 2.0, 3]
route2 = [3, 4, 5]
route3 = [5, 6, 7]
route4 = [7, 8, 1]

route1.pop()

"""