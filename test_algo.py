# from optim_gen import run_vrptw
import pandas as pd
instance = pd.read_csv('entrepot_1.csv')
instance.drop(['Unnamed: 0', 'Identifiant'], axis = 'columns', inplace = True)
n = instance.shape[1]
number_of_points = n - 3
instance.columns = ['vehicle_capacity', 'max_vehicle', 'demand'] + [i for i in range(number_of_points)]
print(instance.head())

distance_matrix = instance[i for i in range(3,n)] #prend la matrice des colonnes
