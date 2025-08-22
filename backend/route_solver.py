import json
import math
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp




def dataExtraction(filename="data3.json"):
    """Load JSON input data"""


    with open(filename,"r") as f:
        data = json.load(f)
    
    return data


def haversine(lat1, lon1, lat2, lon2):
    """compute disntace between 2 lat/lng pair in meters"""
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    return R * 2 * math.asin(math.sqrt(a)) * 1000  # in meters

def computeDistanceMatrix(coords):
    """compute the distance matrix for given coordinates"""

    distance_matrix = []
    for from_node in coords:
        row = []
        for to_node in coords:
            distanceBtwNodes = haversine(from_node['lat'],from_node['lng'],
                                        to_node['lat'],to_node['lng']
                                         )

            row.append(int(distanceBtwNodes))#passing int value
        distance_matrix.append(row)
    return distance_matrix


def createDataModel(coords,numberOfVehicles):
    """OR tool data model"""
    return {
        'distance_matrix': computeDistanceMatrix(coords),
        'num_vehicles': numberOfVehicles,
        'depot': 0,
    }


def solvingVRP(coords, numberOfVehicles, maxDistancePerVehicle=None):
    """Simplified VRP with forced vehicle usage"""


    #Parameters: (total_locations, number_of_vehicles, depot_index
    data = createDataModel(coords, numberOfVehicles)
    
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'],
                                           data['depot'])
    routing = pywrapcp.RoutingModel(manager)
    

    #looks up distance between the asked nodes
    def distanceCallback(fromIndex, toIndex):
        return data['distance_matrix'][manager.IndexToNode(fromIndex)][manager.IndexToNode(toIndex)]

    #tells or-tools to use distancecall back function 
    transitIndex = routing.RegisterTransitCallback(distanceCallback)

    #All vehicles use the same distance costs
    routing.SetArcCostEvaluatorOfAllVehicles(transitIndex)
    


    #calc the dymaic penalty:
    distance_matrix = data['distance_matrix']
    avgDistance = sum(sum(row) for row in distance_matrix) / (len(coords) **2)
    #dynamic penalty
    vehiclePenalty = int(avgDistance * 1.5) #150% of avg distance seems fare
    

    #  High penalty for unused vehicles
    for vehicle_id in range(numberOfVehicles):
        routing.SetAmortizedCostFactorsOfVehicle(1, vehiclePenalty, vehicle_id)
    
    #this forces the device to use all the vehicles 
    if maxDistancePerVehicle:
       routing.AddDimension(transitIndex, 0, maxDistancePerVehicle, True, 'Distance')

       distance_dimension = routing.GetDimensionOrDie('Distance')
       distance_dimension.SetGlobalSpanCostCoefficient(100)  # Balance routes!
    
    
    searchParams = pywrapcp.DefaultRoutingSearchParameters()
    searchParams.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION
    searchParams.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    searchParams.time_limit.FromSeconds(30)
    
    solution = routing.SolveWithParameters(searchParams)
    
    routes = []
    if solution:
        for vehicle_id in range(data['num_vehicles']):
            route = []
            index = routing.Start(vehicle_id)
            while not routing.IsEnd(index):
                route.append(manager.IndexToNode(index))
                index = solution.Value(routing.NextVar(index))
            route.append(manager.IndexToNode(index))
            routes.append(route)
    else:
        # Fallback: Equal distribution
        routes = [[0, 0] for _ in range(numberOfVehicles)]
        deliveries = list(range(1, len(coords)))
        for i, delivery in enumerate(deliveries):
            vehicle_id = i % numberOfVehicles
            if len(routes[vehicle_id]) == 2:  # Only depot-depot
                routes[vehicle_id] = [0, delivery, 0]
            else:
                routes[vehicle_id].insert(-1, delivery)  # Insert before final depot
    
    return routes
 


if __name__ == "__main__":



    #loading data
    rawData = dataExtraction("data3.json")
    coords = rawData['coordinates']
    numberOfVehicles = rawData['numberOfVehicles']
    maxDistancePerVehicle = rawData['maxDistancePerVehicle']


    routes = solvingVRP(coords,numberOfVehicles,maxDistancePerVehicle)


    output = {
        "routes": routes,
        "coordinates":coords
    }


    print(json.dumps(output,indent=2))



