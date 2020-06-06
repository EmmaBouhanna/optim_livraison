import pandas as pd
from optim_gen import run_vrptw
instance = pd.read_csv('entrepot_1.csv')
instance.drop(['Unnamed: 0', 'Identifiant'], axis = 'columns', inplace = True)
n = instance.shape[1]
number_of_points = n - 3
number_of_clients = number_of_points - 1
instance.columns = ['vehicle_capacity', 'max_vehicle', 'demand'] + [i for i in range(number_of_points)]
print(instance.head())

distance_matrix = instance[[i for i in range(0,number_of_points)]] #prend la matrice des colonnes
print(distance_matrix.head())

run_vrptw(instance, distance_matrix, 1.0, 1.0, number_of_clients, 100, 0.4, 0.2, 10)