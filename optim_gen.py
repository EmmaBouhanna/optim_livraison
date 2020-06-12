import numpy as np
import random
import pandas as pd
import csv
import os
path = 'C:\Didou\Pro\devoirs\Mines\Projet info S2\optim_livraison'
# N camions => N 'individus'
# Un individu : liste des clients visités dans l'ordre par x camions (où x < N)
# une route : décode l'individu en [[4,5,2], [6,7], [10]] (Trois camions ont livré)
# tous les camions ont la même capacité au départ

service_time = (1/6) # 10 min pour déposer le colis
time_work = 8 #journée de travail du camionneur est de 8h

def truck_division(file_properties):
    n = len(file_properties)
    number_trucks_from_garage = file_properties.pop()
    deliveries_per_warehouse = file_properties[2::3]
    max_truck_per_warehouse = file_properties[1::3]
    number_deliveries = np.sum(np.array(deliveries_per_warehouse))
    weight_of_delivery = number_trucks_from_garage/number_deliveries
    number_truck_per_warehouse = []
    counter = 0
    k = 0
    for truck,demand in zip(max_truck_per_warehouse,deliveries_per_warehouse):
        new_number_trucks = int(demand*weight_of_delivery)
        if demand<truck and demand<=number_trucks_from_garage - counter:
            number_truck_per_warehouse.append(demand)
            counter += demand
        else:
            if k == len(deliveries_per_warehouse):
                number_truck_per_warehouse.append(number_trucks_from_garage - counter)
            elif new_number_trucks<truck:
                number_truck_per_warehouse.append(new_number_trucks)
                counter += new_number_trucks
            elif new_number_trucks>=truck:
                number_truck_per_warehouse.append(truck)
                counter += truck
        k += 1
    return(number_truck_per_warehouse)


    


''' Décodage d'un individu en route'''
def ind2route(individual, instance, distance_matrix, vehicle_capacity, max_vehicle, initCost, serviceTime = service_time):
    # init_cost = time to go from the garage to the warehouse and to come back
    route = []
    vehicleCapacity = vehicle_capacity
    # Initialize a sub-route
    subRoute = [0]
    vehicleLoad = 0
    lastCustomerID = 0
    elapsedTime = 2*initCost
    for customerID in individual:
        # Update vehicle load
        demand = instance['demand'][customerID]
        updatedVehicleLoad = vehicleLoad + demand
        # Update elapsed time
        returnTime = distance_matrix[customerID][0] #distance_matrix = distance entre i et j
        updatedElapsedTime = elapsedTime + distance_matrix[lastCustomerID][customerID] + serviceTime + returnTime
        # Validate vehicle load and elapsed time
        if (updatedVehicleLoad <= vehicleCapacity) and (updatedElapsedTime <= time_work):
            # Add to current sub-route
            subRoute.append(customerID)
            vehicleLoad = updatedVehicleLoad
            elapsedTime = updatedElapsedTime - returnTime
        else:
            # Save current sub-route
            subRoute.append(0)
            route.append(subRoute)
            # Initialize a new sub-route and add to it
            subRoute = [0, customerID]
            vehicleLoad = demand
            elapsedTime = distance_matrix[0][customerID] + serviceTime
        # Update last customer ID
        lastCustomerID = customerID
    if subRoute != []:
        # Save current sub-route before return if not empty
        subRoute.append(0)
        route.append(subRoute)
    route = route[1:]
    if max_vehicle < len(route):
        raise ValueError
    return (route)

''' Pour afficher une route avec les allers-retours d'un camion'''
def printRoute(route, merge=False):
    routeStr = '0'
    subRouteCount = 0
    for subRoute in route:
        subRouteCount += 1
        subRouteStr = '0'
        for customerID in subRoute:
            subRouteStr = subRouteStr + ' - ' + str(customerID)
            routeStr = routeStr + ' - ' + str(customerID)
        subRouteStr = subRouteStr + ' - 0'
        if not merge:
            print('  Vehicle %d\'s route: %s' % (subRouteCount, subRouteStr))
        routeStr = routeStr + ' - 0'
    if merge:
        print(routeStr)
    return

'''Création du coût d'un parcours, qu'il faudra par la suite optimiser'''
# unit_cost : on attribue aux camions un coût par unité de déplacement
def evalVRPTW(individual, instance, distance_matrix, vehicle_capacity, max_vehicle, unitCost=1.0, initCost=0):
    #init_cost : cost to travel from the parking to the warehouse
    totalCost = 0
   
    route = ind2route(individual, instance, distance_matrix, vehicle_capacity, max_vehicle, initCost)
    
    totalCost = 0
    for subRoute in route:
        subRouteDistance = 0
        elapsedTime = 0
        lastCustomerID = 0
        for customerID in subRoute:
            # Calculate section distance
            distance = distance_matrix[lastCustomerID][customerID]
            # Update sub-route distance
            subRouteDistance = subRouteDistance + distance
            # Calculate time cost
            arrivalTime = elapsedTime + distance
            # Update elapsed time
            elapsedTime = arrivalTime + service_time
            # Update last customer ID
            lastCustomerID = customerID
        # Calculate transport cost
        subRouteDistance = subRouteDistance + distance_matrix[lastCustomerID][0]
        subRouteTranCost = initCost + unitCost * subRouteDistance
        # Update total cost
        totalCost = totalCost + subRouteTranCost
    fitness = 1.0 / totalCost
    return fitness

#on va chercher à maximiser fitness

'''Implémentation de la fonction de crossover lors de l'évolution génétique '''

def cx_partialy_matched(ind1, ind2):
    size = min(len(ind1), len(ind2))
    try:
        cxpoint1, cxpoint2 = sorted(random.sample(range(size), 2))
    except ValueError:
        print('Error : Only one package to deliver')
    temp1 = ind1[cxpoint1:cxpoint2+1] + ind2
    temp2 = ind1[cxpoint1:cxpoint2+1] + ind1
    ind1 = []
    for gene in temp1:
        if gene not in ind1:
            ind1.append(gene)
    ind2 = []
    for gene in temp2:
        if gene not in ind2:
            ind2.append(gene)
    return ind1, ind2

'''Implémentation de la fonction de mutation lors du processus génétique'''
# On fait l'hypothèse de mutation par inversion seulement (ie pas d'insertion ni de déletion, plus simple car on a des cleints fixes à livrer
# Et le seul facteur sur lequel on peut jouer est l'ordre de livraison
def mut_inverse_indexes(individual):
    '''gavrptw.core.mut_inverse_indexes(individual)'''
    start, stop = sorted(random.sample(range(len(individual)), 2))
    individual = individual[:start] + individual[stop:start-1:-1] + individual[stop+1:]
    return (individual, )



'''Création de l'algorithme génétique (utilisation de la libraire deep tools)'''
from deap import tools, creator, base

def run_vrptw(instance, distance_matrix, vehicle_capacity, max_vehicle, unit_cost, init_cost, ind_size, pop_size, \
    cx_pb, mut_pb, n_gen):
    #ind_size = le nombre de clients !
    #cx_pb = probability of cross-over
    #mut_pb = probability of a mutation
    creator.create("FitnessMax", base.Fitness, weights = (1.0,) ) #on prend des poids porsitifs car on veut maximiser fitness
    creator.create('Individual', list, fitness=creator.FitnessMax)
    toolbox = base.Toolbox()  # on initialise une instance de l'objet Toolbox
    toolbox.register('indexes', random.sample, range(1, ind_size + 1), ind_size) #on crée un générateur qui va les numéros des clients à livrer (codés de 1 à ind_size, à décoder éventuellement)
    toolbox.register('individual', tools.initIterate, creator.Individual, toolbox.indexes) #crée un individu en appelant la fonction random.sample(range(1,ind_size+1), ind_size)
    toolbox.register('population', tools.initRepeat, list, toolbox.individual) 
    pop = toolbox.population(n=pop_size) #on crée une population de m individus qui nous sert de départ pour l'algo génétique

    #évaluation du coût
    toolbox.register('evaluate', evalVRPTW, instance=instance, distance_matrix=distance_matrix, vehicle_capacity = vehicle_capacity, max_vehicle = max_vehicle,unitCost=unit_cost, initCost=init_cost)

    #sélection de k individus dans la population
    toolbox.register('select', tools.selRoulette)

    #Association de deux individus de la population
    toolbox.register('mate', cx_partialy_matched)

    #Mutation d'un individu
    toolbox.register('mutate', mut_inverse_indexes)
    
    print('start of evolution')
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses): #on stocke le coût pour chaque individu dans les atribus du creator Individual
        ind.fitness.values = (fit,)
    print(f'Evaluated {len(pop)} individuals')

    # Begin the evolution
    for gen in range(n_gen):
        print(f'-- Generation {gen} --')
    
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop)) # Every individual is able to move on to the next generation

        # Clone the selected individuals (to avoid modification of the real pop)
        offspring = list(map(toolbox.clone, offspring))
        

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]): #liste[start : stop : step]
            # On apparie potentiellent l'individu n à l'individu n+1
            if random.random() < cx_pb: # Proba qu'il y ait un crossover
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values
                # On a modifié child1 et child2, ils ont maintenant des fitness.values invalides (les enfants se sont croisés)
        for mutant in offspring: # Proba d'une mutation
            if random.random() < mut_pb:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = (fit,)
        print(f'  Evaluated {len(invalid_ind)} individuals')

        # The population is entirely replaced by the offspring
        pop[:] = offspring

    print('-- End of (successful) evolution --')
    best_ind = tools.selBest(pop, 1)[0] #returns a list containing the k best individuals among the population, here the best one
    print(f'Best individual: {best_ind}')
    print(f'Fitness: {best_ind.fitness.values[0]}')
    print(f'Total cost: {1 / best_ind.fitness.values[0]}')
    return( ind2route(best_ind, instance, distance_matrix, vehicle_capacity, max_vehicle, init_cost))


'''Exportation des résultats'''
def decode_to_GPS(liste_res, instances):
    entrepot_num = 0
    for (routes_entrepot,instance) in zip(liste_res,instances):
        entrepot_num += 1
        for route in routes_entrepot:
            for i in range(len(route)):
                route[i] = (instance['latitude'][route[i]], instance['longitude'][route[i]])
        name = 'res_entrepot_' + str(entrepot_num) + '.csv'
        columns_res = ['camion' + str(k+1) for k in range(len(routes_entrepot))]
    
        res = pd.DataFrame(routes_entrepot, index = columns_res).transpose()
        res.to_csv(os.path.join(path,'output_data',name))