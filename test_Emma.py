from graphe import *
from optim_gen import run_vrptw, decode_to_GPS

g = Garage (2.2728354, 48.8281142997349, 40, 60)
c = Camion(50, 0, 10000)

k = 10 # choose number of clients
df, warehouses, parcels = create_graph_components(k)

G = Graph(g, warehouses, parcels, c)
G.make_graph()
file_properties = G.generate_csv()
print(file_properties)
vehicle_capacity= file_properties.pop()
max_vehicle_per_warehouse = file_properties[1::3]

truck_div = truck_division(file_properties)
print(truck_div)
instances = [] #listes pour regrouper les résultats par entrepot
liste_res =[]

for (i, file) in enumerate(file_properties[::3]):
    instance = pd.read_csv(os.path.join(PATH, 'input_data', file))
    if instance.shape[0]>2 :
        instances += [instance]
    print(instance.head())
    max_vehicle = truck_div[i]
    instance_bis = instance.drop(['Unnamed: 0', 'Identifiant', 'latitude', 'longitude'], axis = 'columns')
    n = instance_bis.shape[1]
    number_of_points = n - 1
    number_of_clients = number_of_points - 1
    instance_bis.columns = ['demand'] + [i for i in range(number_of_points)]

    distance_matrix = instance_bis[[i for i in range(0,number_of_points)]] #prend la matrice des colonnes
    try :
        res = run_vrptw(instance_bis, distance_matrix, vehicle_capacity, max_vehicle, 1.0, number_of_clients, 100, 0.4, 0.2, 10)
        liste_res.append(res)
    except Exception:
        print('Oooops') # only one package to deliver    


decode_to_GPS(liste_res, instances)

