from __init__ import *
from graphe_sans_osmnx import * 
service_time = (1/6) # 10 min lost per delivery
time_work = 8.0 # number of work hours
cost_dist = 1/3600 # coût par unité de temps

'''
This part is coded in case we want to consider that all the trucks don't start their day directly
in the warehouse

def truck_division(file_properties):
    """
    Trucks that come from the garage are divided into the warehouses before starting their deliveries.

    Input : a list containing the names of the warehouses, the maximal number of trucks allowed each warehouse and the number
    of deliveries per warehouse.
    Output : Returns a list containing the number of vehicles per warehouse at the beginning of the day

    """
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

'''
def no_client_to_deliver(file):
    '''
    Determines if there are packages to deliver from each warehouse at the beginning of the day

    Input :  file (list) containing the names of the warehouses, the maximal number of trucks 
    allowed in each warehouse and the number of deliveries per warehouse.
    Output : file_2 (list) containing the names of the warehouse, the maximal number of trucks 
    allowed in each warehouse and the number of deliveries per warehouse if non zero.
    '''
    file_2 = []
    for i in range(1, len(file)//3 +1):
        if file[3*i-1] != 0:
            file_2.append(file[3*(i-1)])
            file_2.append(file[3*i-2])
            file_2.append(file[3*i-1])
    return(file_2)

def one_client_to_deliver(file):
    '''
    Solve the problem directly if there is only one client to deliver by exporting csv containg the results

    Input : file (list) containing the names of the warehouses, the maximal number of trucks 
    allowed in each warehouse and the number of deliveries per warehouse.
    Output : file (list) containing the names of the warehouses, the maximal number of trucks 
    allowed in each warehouse and the number of deliveries per warehouse if non 1
    '''
    file_2 = []
    for i in range(1, len(file)//3 +1):
        if file[3*i-1] == 1:
            instance = pd.read_csv(os.path.join(PATH,'input_data',file[3*(i-1)]))
            columns_res = ['Camion 1']
            res = [instance['Identifiant'][i] for i in [0,1,0]]
            print(res)
            res = pd.DataFrame(res, columns = columns_res)
            res.to_csv(os.path.join(PATH,'output_data', 'res_entrepot_' + str(instance['Identifiant'][0]) +'.csv' ))
        else :
            file_2 += file[3*(i-1):3*i]
    return(file_2)



def ind2route(individual, instance, distance_matrix, vehicle_capacity, max_vehicle, initCost = 0.0, unitCost = cost_dist, serviceTime = service_time):
    """
    Decoding individual to route

    Input : 
    - individual : list to be decoded into a route containing
    the journey of each truck which started at the warehouse
    - instance : dataframe containing the demand of each client (volume of package), latitude and longitude of each point (warehouse + destinations)
    - distance_matrix : dataframe containing the distances between client i and client j (the cost to travel from i to j)
    - vehicle capacity (float) : total volume that can be loaded in the trucks (every truck have the same capacity for the moment)
    - max_vehicle (int) : number of trucks in the warehouse at the beginning of the day
    - init_cost (float) : in case we want to include the trip from home to work to the worker's day 
    (default = 0)
    - serviceTime : time lost per delivery

    Output : a list of lists containing the route of each truck from the warehouse and back to it at the end of the day

    """
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
        returnTime = distance_matrix[customerID][0]*unitCost #distance_matrix = distance entre i et j
        updatedElapsedTime = elapsedTime + distance_matrix[lastCustomerID][customerID]*unitCost + serviceTime + returnTime
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
            elapsedTime = distance_matrix[0][customerID]*unitCost + serviceTime
        # Update last customer ID
        lastCustomerID = customerID
    if subRoute != []:
        # Save current sub-route before return if not empty
        subRoute.append(0)
        route.append(subRoute)
    if max_vehicle < len(route):
        raise ValueError
    return (route)

def printRoute(route, merge=False):
    """
    Print a route with the journey of each truck (to check)

    Input : a route (list)
    Output : None 
    """ 
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

def evalVRPTW(individual, instance, distance_matrix, vehicle_capacity, max_vehicle, unitCost=cost_dist, initCost=0.0):
    """
    Creation of a cost function based on the total cost of each route

    Input :
    - individual : list containing the total journey of the trucks (has to be decoded afterwards to get the real journey of each truck)
    - instance : dataframe containing the demand of each client (volume of package), longitude and latitude of each point (warehouse + destinations)
    - distance_matrix : dataframe containing the distances between client i and client j (the cost to travel from i to j)
    - vehicle capacity (float) : total volume that can be loaded in the trucks (every truck have the same capacity for the moment)
    - unitCost (float) : cost of 1 unity of movement
    - init_cost (float) : in case we want to include the trip from home to work to the worker's day 
    (default = 0)

    Output : Fitness (1/Cost)
    """
   
    route = ind2route(individual, instance, distance_matrix, vehicle_capacity, max_vehicle)
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

# We intend to maximise fitness

def cx_partialy_matched(ind1, ind2):
    '''
    Step of the genetic algorithm : crossover

    Input : two individuals (list)
    Output : two individuals that have been modified
    '''
    size = min(len(ind1), len(ind2))
    try:
        cxpoint1, cxpoint2 = sorted(random.sample(range(size), 2))
    except ValueError:
        print('Error : Only one package to deliver')
    temp1 = ind1[cxpoint1:cxpoint2+1] + ind2
    temp2 = ind2[cxpoint1:cxpoint2+1] + ind1
    ind1 = []
    for gene in temp1:
        if gene not in ind1:
            ind1.append(gene)
    ind2 = []
    for gene in temp2:
        if gene not in ind2:
            ind2.append(gene)
    return ind1, ind2

def mut_inverse_indexes(individual):
    '''
    Step of genetic algorithm : Mutation (only by inversion, to keep the unicity of each occurence) . No insertion or deletion allowed

    Input : individual (list)
    Output : mutated individual
    '''

    start, stop = sorted(random.sample(range(len(individual)), 2))
    individual = individual[:start + 1] + individual[stop:start:-1] + individual[stop+1:]
    return (individual, )


def run_vrptw(instance, distance_matrix, vehicle_capacity, max_vehicle, ind_size, pop_size, \
    cx_pb, mut_pb, n_gen, init_cost = 0.0, unit_cost = cost_dist):
    """
    Genetic algorithm which combines all the step of the process of evolution

    Input : 
    - instance : dataframe containing the demand of each client (volume of package)
    - distance_matrix : dataframe containing the distances between client i and client j (the cost to travel from i to j)
    - vehicle capacity (float) : total volume that can be loaded in the trucks (every truck have the same capacity for the moment)
    - max_vehicle (int) : number of trucks in the warehouse at the beginning of the day
    - ind_size (int) : number of clients
    - pop_size (int) : size of the population
    - cx_pb (float) : probability of crossover
    - mut_pb(float) : probability of mutation
    - n_gen (int) : number of generations
    - init_cost (float) : in case we want to include the trip from home to work to the worker's day 
    (default = 0)
    - unit_cost (float) : temporal cost of 1 unity of distance
    """

    creator.create("FitnessMax", base.Fitness, weights = (1.0,) ) #Positive weights because we intend to maximise fitness
    creator.create('Individual', list, fitness=creator.FitnessMax)
    
    # Instance of Toolbox object
    toolbox = base.Toolbox() 

    # Creation of generator that generates the numbers of customers to deliver (coded from 1 to ind_size, potentially to decode)
    toolbox.register('indexes', random.sample, range(1, ind_size + 1), ind_size)

    # Creation of an indicidual by calling random.sample(range(1,ind_size+1), ind_size)
    toolbox.register('individual', tools.initIterate, creator.Individual, toolbox.indexes)

    # Creation of a population made up of n individuals : start of the genetic algorithm
    toolbox.register('population', tools.initRepeat, list, toolbox.individual) 
    pop = toolbox.population(n=pop_size) 

    # Cost Evaluation
    toolbox.register('evaluate', evalVRPTW, instance=instance, distance_matrix=distance_matrix, vehicle_capacity = vehicle_capacity, max_vehicle = max_vehicle,unitCost=unit_cost, initCost=init_cost)

    # Selection of k individuals from the population
    toolbox.register('select', tools.selRoulette)

    # Association of two individuals from the population
    toolbox.register('mate', cx_partialy_matched)

    # Mutation of an individual
    toolbox.register('mutate', mut_inverse_indexes)
    
    print('start of evolution')
    print(pop)
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses): #Keep track of each indiviual's cost as attributes of creator Individual
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
        for child1, child2 in zip(offspring[::2], offspring[1::2]): #list[start : stop : step]
            # potentially match individual n and individual n+1
            if random.random() < cx_pb: # Probability of a crossover
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values
                # changed child1 et child2, they now have invalid fitness.values (children have crossed)
        for mutant in offspring: # Probability of mutation
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
        best_ind = tools.selBest(pop, 1)[0]  #returns a list containing the k best individuals among the population, here the best one
        print(f'Best Fitness at Generation {gen}: {best_ind.fitness.values[0]}')

    print('-- End of (successful) evolution --')
    best_ind = tools.selBest(pop, 1)[0]  #returns a list containing the k best individuals among the population, here the best one
    print(f'Best individual: {best_ind}')
    print(f'Total cost: {1 / best_ind.fitness.values[0]}')
    return( ind2route(best_ind, instance, distance_matrix, vehicle_capacity, max_vehicle))

def decode_to_GPS(liste_res, instances):
    """
    Export results

    Input: 
    - list_res (list) : Results of the algorithm for each warehouse
    - instances(list of dataframes) : keeps track of all the instances of each warehouse
    Output : None

    """
    warehouse_num = 0
    for (routes_warehouse,instance) in zip(liste_res,instances):
        warehouse_num += 1
        for route in routes_warehouse:
            for i in range(len(route)):
                route[i] = instance['Identifiant'][route[i]]
        name = 'res_entrepot_' + str(instance['Identifiant'][0]) +'.csv'
        columns_res = ['camion' + str(k+1) for k in range(len(routes_warehouse))]
        print(routes_warehouse)
        res = pd.DataFrame(routes_warehouse, index = columns_res).transpose()
        res.to_csv(os.path.join(PATH,'output_data',name))


def simulation_vrptw(garage, truck, number_clients):
    '''
    Produce the results of the algorithm using a graph and all the funcntions implemented before

    Input : 
    - garage(class Garage from graphe.py)
    - truck (class Camion from graphe.py)
    - number_clients (int) : total number of clients to deliver during the day

    Output : None, the results are in the folder 'output_data'
    '''
    df, indexes, warehouses, parcels = create_graph_components(number_clients)
    G = Graph(garage, warehouses, parcels, truck)
    G.make_graph()
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

