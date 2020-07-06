

import os
import folium
import pandas as pd
import osmnx as ox

from routes import *

"""
This module contains functions to visualize the results of the algorithm
on folium maps.
"""

# Coordinates of Paris' center
Paris_center = [48.861146, 2.345721]

# Load result dataframe containing warehouses and clients
df_complete = pd.read_csv('./output_data_bis/df_complete.csv', 
usecols = ["y", "x", "name", "type", "adress"])

# Dictionaries of latitudes and longitudes 
# key : osmid (int) ; value : latitude or longitude (float)
Lats_node_id = nx.get_node_attributes(G_idf, "y")
Lons_node_id = nx.get_node_attributes(G_idf, "x")

# Lists of latitudes and longitudes 
# sorted by index of the dataframe containing warehouses and clients (df_complete)
Lats_df_id = list(df_complete["y"])
Lons_df_id = list(df_complete["x"])


# Create list containing "res_entrepot_i" files
files_list = []
for (root, dirs, files) in os.walk('./output_data'):
    files_list.extend(files)

if '.DS_Store' in files_list :
    files_list.remove('.DS_Store')


# Load dictionary containing all-pairs itineraries

df_itineraries = pd.read_csv('./output_data_bis/itineraries_dict.csv', header=None)
itineraries_dict = {}

for i in range(df_itineraries.shape[1]) :
    # pre-treating data because the dictionary was saved as several strings
    cleaned_ = df_itineraries[i][1].split('[')[1]
    cleaned_ = cleaned_.split(']')[0]
    route = cleaned_.split(', ')
    for j in range(len(route)) :
        route[j] = int(route[j])
    itineraries_dict[df_itineraries[i][0]] = route



def random_color():

    """
    Return a random rgb color code
    """
    levels = range(32,256,32)
    return f"rgb{tuple(random.choice(levels) for _ in range(3))}"



def visualize_nearest_nodes(df, input_map = None, n_warehouses=None) : 

    """
    Display on a map all geographical points of a dataframe and their respective
    nearest osm nodes.

    Input:
    - df (pandas.DataFrame) : dataframe 
    - my_map (folium.Map, optional) : if specified, the geographical points and nodes
    will be displayed on this pre-existing map

    Output :
    - my_map (folium.Map) : a map displaying the geographical points and nearest nodes
    """

    n = df.shape[0]

    coords_list, nearest_nodes_list = nearest_nodes(df)

    # Create a folium map if no map in input
    if input_map is None :
        my_map = folium.Map(location = Paris_center, 
                    tiles='Stamen Toner', zoom_start = 9, control_scale=True)
    
    else :
        my_map = input_map

    # All points are treated the same way if the number of warehouses is not specified
    if n_warehouses is None :
    
        for k in range(n):

            folium.Circle(radius=100, location=coords_list[k], color='red',
                    fill=False).add_to(my_map)

            folium.Circle(radius=150, 
                    location=(Lats_node_id[nearest_nodes_list[k]], Lons_node_id[nearest_nodes_list[k]]), 
                    color='blue',
                    fill=False).add_to(my_map)

    # Difference of display between warehouses and clients if the number of warehouses is specified
    else : 
        
        #warehouses
        for k in range(n_warehouses):

            folium.Circle(radius=100, location=coords_list[k], color='red',
                    fill=False).add_child(folium.Popup(f'entrepot {k}', show = True)).add_to(my_map)

            folium.Circle(radius=150, 
                    location=(Lats_node_id[nearest_nodes_list[k]], Lons_node_id[nearest_nodes_list[k]]), 
                    color='orange',
                    fill=False).add_child(folium.Popup(f'noeud entrepot {k}', show = False)).add_to(my_map)

        #clients
        for k in range(n_warehouses, n):

            folium.Circle(radius=100, location=coords_list[k], color='blue',
                    fill=False).add_child(folium.Popup(f'client {k - n_warehouses}', show = True)).add_to(my_map)

            folium.Circle(radius=150, 
                    location=(Lats_node_id[nearest_nodes_list[k]], Lons_node_id[nearest_nodes_list[k]]), 
                    color='green',
                    fill=False).add_child(folium.Popup(f'noeud client {k - n_warehouses}', show = False)).add_to(my_map)

    return my_map




def visualize_travel_between_two_nodes(start, end, line_color='red', input_map=None, G=G_idf) :
    
    """
    Draw the path between two nodes on a folium map

    Input :
    - start (int) : index (in the dataframe) of the start point 
    - end (int) : index (in the dataframe) of the start point 
    - line_color (str) : color used to draw the path
    - input_map (folium.Map) : if specified, the path will be drawn on this pre-existing map
    - G (networkx.MultiDiGraph) : the graph that has been used to calculate the routes

    Output :
    - my_map (folium.Map) : a map on which the path is drawn
    
    """

    if input_map is None :
        my_map = folium.Map(location = Paris_center,
                    tiles='Stamen Toner', zoom_start = 9, control_scale=True)
    
    else :
        my_map = input_map

    path = itineraries_dict[f'({start}, {end})']

    # Draw the route
    ox.folium.plot_route_folium(G, path, route_map=my_map, tiles='Stamen Toner', 
                            popup_attribute = "name", zoom = 9,
                            route_color = line_color,
                            route_width=7, route_opacity=0.7)

    # Display start point
    folium.Circle(radius=200, 
                location=(Lats_df_id[start], Lons_df_id[start]), 
                color='green',
                fill=True).add_child(folium.Popup(f'{start}', show = True)).add_to(my_map)

    # Display end point
    folium.Circle(radius=200, 
                location=(Lats_df_id[end], Lons_df_id[end]), 
                color='green',
                fill=True).add_child(folium.Popup(f'{end}', show = True)).add_to(my_map)
   
    return my_map



def visualize_single_truck_travel(stops_list, color='red', input_map_=None, G=G_idf):

    """
    Draw the itinerary of a truck on a folium map

    Input :
    - stops_list (list) : list of dataframe indexes of the nodes visited by the truck
    - line_color : color used to draw the path
    - input_map : if specified, the path will be drawn on this pre-existing map
    - G (networkx.MultiDiGraph) : the graph that has been used to calculate the routes

    Output :
    - my_map : a map on which the route of the truck is drawn. The different stops are 
    indicated by pop-ups

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



def visualize_single_warehouse_travel(res_csv, preexisting_map=None, G=G_idf) :

    """
    Draw the itineraries of all trucks from a warehouse on a folium map

    Input :
    - res_csv : the csv file containing paths of all trucks for a single warehouse.
    Available files can be found in files_list
    - preexisting_map (folium.Map) : if specified, the paths will be drawn on this pre-existing map
    - G (networkx.MultiDiGraph) : the graph that has been used to calculate the routes

    Output :
    - my_map (folium.Map) : a map on which the paths are drawn. A different color is used for each truck
    
    """

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
    folium.Circle(radius=300, location=(Lats_df_id[warehouse], Lons_df_id[warehouse]), color='red',
                    fill=False).add_child(folium.Popup(f'entrepot {warehouse}', show = True)).add_to(output_map)

    for truck in trucks_list :
        # a different color for each truck
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