from graphe_sans_osmnx import *
from optim_gen import *
g = Garage(2.2728354, 48.8281142997349, 40, 60)
c = Camion(1, 0, 10000)
df, indexes, warehouses, parcels = create_graph_components(50)
G = Graph(g, warehouses, parcels, c)
G.make_graph()
G.make_dist_matrix(df)

# Save dataframe, dist_matrix and itineraries_dict
df.to_csv(os.path.join(PATH,'output_data_bis/df_complete.csv'))

if G.matrix is not None :
    np.savetxt(os.path.join(PATH, 'output_data_bis/corrected_travel_times_array.csv'), G.matrix, delimiter=",")

if G.itineraries is not None :
    with open(os.path.join(PATH,'output_data_bis/itineraries_dict.csv'), 'w') as f:  
        w = csv.DictWriter(f, G.itineraries.keys())
        w.writeheader()
        w.writerow(G.itineraries)

file_properties = generate_csv(G, df, indexes)
vehicle_capacity= file_properties.pop()
file_properties = no_client_to_deliver(file_properties)
file_properties = one_client_to_deliver(file_properties)
trucks = file_properties[1::3]
number_clients_per_warehouse = file_properties[2::3]
instances = [] #listes pour regrouper les résultats par entrepot
liste_res =[]
for (i, file) in enumerate(file_properties[::3]):
    instance = pd.read_csv(os.path.join(PATH, 'input_data', file))
    if instance.shape[0]>2 :
        instances += [instance]
    print(instance.head())
    max_vehicle = trucks[i]
    instance_bis = instance.drop(['Unnamed: 0', 'Identifiant', 'latitude', 'longitude'], axis = 'columns')
    n = instance_bis.shape[1]
    number_of_points = n - 1
    number_of_clients = number_clients_per_warehouse[i]
    instance_bis.columns = ['demand'] + [i for i in range(number_of_points)]
    distance_matrix = instance_bis[[i for i in range(0,number_of_points)]] #prend la matrice des colonnes
    res = run_vrptw(instance_bis, distance_matrix, vehicle_capacity, max_vehicle, number_of_clients, 100, 0.4, 0.2, 200)
    liste_res.append(res)

decode_to_GPS(liste_res, instances)