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

            row.append(distanceBtwNodes)
        distance_matrix.append(row)
    return distance_matrix


def createDataModel(coords,numberOfVehicles):
    """OR tool data model"""
    return {
        'distance_matrix': computeDistanceMatrix(coords),
        'num_vehicles': numberOfVehicles,
        'depot': 0,
    }


def solvingVRP(coords,numberOfVehicles,maxDistancePerVehicle=None):
    """Using the standard OR tools technices to solve the VRP"""

    data = createDataModel(coords,numberOfVehicles)

    #setup manager and routing
    # Setup manager and routing
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'],
                                           data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    #distance callback:
    def distanceCallback(fromIndex, toIndex):
        return data['distance_matrix'][manager.IndexToNode(fromIndex)][manager.IndexToNode(toIndex)]

    transitIndex = routing.RegisterTransitCallback(distanceCallback)
    routing.SetArcCostEvaluatorOfAllVehicles(transitIndex)


    #max distance params :
    if maxDistancePerVehicle:
        routing.AddDimension(
            transitIndex,
            0,
            maxDistancePerVehicle,
            True,
            'Distance'
        )

    # Search parameters
    searchParams = pywrapcp.DefaultRoutingSearchParameters()
    searchParams.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

    #solve
    solution = routing.SolveWithParameters(searchParams)

     # Extract routes
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
        print("No solution found! Try adjusting maxDistancePerVehicle or reducing locations")

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














'''
# data extraction
with open('data3.json') as f:
    
    data = json.load(f)
    coords = data['coordinates']
    numberOfVehicles = data['numberOfVehicles']
    maxDistancePerVehicle = data['maxDistancePerVehicle']


# Compute distance matrix
def haversine(lat1, lon1, lat2, lon2):
    # simple haversine function
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    return R * 2 * math.asin(math.sqrt(a)) * 1000  # in meters



distance_matrix = []
for from_node in coords:
    row = []
    for to_node in coords:
        row.append(int(haversine(from_node['lat'], from_node['lng'], to_node['lat'], to_node['lng'])))
    distance_matrix.append(row)


def create_data_model():
    return {
        'distance_matrix': distance_matrix,
        'num_vehicles': numberOfVehicles,
        'depot': 0,
    }

data = create_data_model()
manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['depot'])
routing = pywrapcp.RoutingModel(manager)

def distance_callback(from_index, to_index):
    return data['distance_matrix'][manager.IndexToNode(from_index)][manager.IndexToNode(to_index)]

transit_callback_index = routing.RegisterTransitCallback(distance_callback)
routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)


search_parameters = pywrapcp.DefaultRoutingSearchParameters()
search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC



solution = routing.SolveWithParameters(search_parameters)

routes = []
if solution:
    for vehicle_id in range(data['num_vehicles']):
        route = []
        index = routing.Start(vehicle_id)
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route.append(node_index)
            index = solution.Value(routing.NextVar(index))
        route.append(manager.IndexToNode(index))
        routes.append(route)

if not solution:
    print("No solution found! Try increasing maxDistancePerVehicle or reducing locations")
    routes = []  # Empty routes when no solution

output = {
    "routes": routes,
    "coordinates": coords
}

print(json.dumps(output))
'''