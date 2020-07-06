### Test : warehouses_clients.py ==> OK

import time

from warehouses_clients import *

# Warehouses
df_warehouses

# "random_clients" function 
start_time = time.time()

df_complete, indexes = random_clients(5)

print("Temps d'exécution : %s secondes ---" % (time.time() - start_time))

print(f"indexes : {indexes}")
df_complete


### Test : routes.py ==> OK

from routes import *

# 'nearest_nodes' function

coords_list, nearest_nodes_list = nearest_nodes(df_complete)

print(f'coords_list : {coords_list} \n')
print(f'nearest_nodes_list : {nearest_nodes_list}')

# 'itineraries' function ==> slow but it works

coords_list, weight_array, itineraries_dict = itineraries(df_complete)
print(f'coords_list : {coords_list} \n')
print(f'weight_array : \n {weight_array} \n')
print(f'itineraries_dict : \n {itineraries_dict}')