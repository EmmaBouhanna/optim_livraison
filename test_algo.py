from __init__ import *
from optim_gen import run_vrptw, decode_to_GPS, no_client_to_deliver, one_client_to_deliver

a = ['entrepot_' + str(i+1) + '.csv' for i in range(20)]
b = 20*[50]
c = [2,2,0,0,0,0,2,4,4,0,0,0,4,0,0,0,0,0,0,2,50]
file_properties = []
for i in range(20):
    file_properties.append(a[i])
    file_properties.append(b[i])
    file_properties.append(c[i])
file_properties.append(c[-1])
vehicle_capacity = file_properties.pop()
file_properties = no_client_to_deliver(file_properties)
file_properties = one_client_to_deliver(file_properties)

max_vehicle_per_warehouse = file_properties[1::3]
number_clients_per_warehouse = file_properties[2::3]
instances = [] #listes pour regrouper les résultats par entrepot
liste_res =[]

for (i, file) in enumerate(file_properties[::3]):
    instance = pd.read_csv(os.path.join(PATH, 'input_data_test_main', file))
    if instance.shape[0]>2 :
        instances += [instance]
    print(instance.head())
    max_vehicle = max_vehicle_per_warehouse[i]
    instance_bis = instance.drop(['Unnamed: 0', 'Identifiant', 'latitude', 'longitude'], axis = 'columns')
    n = instance_bis.shape[1]
    number_of_points = n - 1
    number_of_clients = number_clients_per_warehouse[i]
    instance_bis.columns = ['demand'] + [i for i in range(number_of_points)]

    distance_matrix = instance_bis[[i for i in range(0,number_of_points)]] #prend la matrice des colonnes
    res = run_vrptw(instance_bis, distance_matrix, vehicle_capacity, max_vehicle, number_of_clients, 100, 0.4, 0.2, 10)
    liste_res.append(res)

decode_to_GPS(liste_res, instances)

