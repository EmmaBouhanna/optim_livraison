### Test : warehouses_clients.py ==> OK

import time

# Warehouses
df_warehouses

# "random_clients" function 
start_time = time.time()

df_complete, indexes = random_clients(10)

print("Temps d'exécution : %s secondes ---" % (time.time() - start_time))

print(f"indexes : {indexes}")
df_complete


### Test : routes_improved.py

from routes_improved import *

# 'nearest_nodes' function

coords_list, nearest_nodes_list = nearest_nodes(df_complete)

print(coords_list)
print(nearest_nodes_list)

# 'itineraries' function

coords_list, weight_array, itineraries_dict = itineraries(df_complete)