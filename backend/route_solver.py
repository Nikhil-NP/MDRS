import json
import math
from ortools.constraint_solver import routing_enums_pb2 #the simulator/solver
from ortools.constraint_solver import pywrapcp


#read the data.json
with open('data.json') as f:
    coords = json.load(f)


#need to create distance matrix based on lat lgn for each
def haversine(lat1,lon1,lat2,lon2):
    R = 6371
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * \
          math.cos(math.radians(lat2)) * math.sin(dlon / 2) **2
    return R* 2 * math.asin(math.sqrt(a)) * 1000


distance_matrix = []
for from_node in coords:
    row = []
    for to_node in coords:
        row.append(int(haversine(from_node['lat'], from_node['lng'], to_node['lat'], to_node['lng'])))
    distance_matrix.append(row)


def create_data_model():
    return{
        'distance_matrix': distance_matrix,
        'num_vehicles':3,
        'depot':0,
    }

data = create_data_model()

#mapping realdata notes to or-internal indecied
manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),data['num_vehicles'],data['depot'])
#solving
routing = pywrapcp.RoutingModel(manager)


#getting distnace between points from  distance_matrix
def distance_callback(from_index,to_index):
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
            route.append(manager.IndexToNode(index))
            routes.append(route)
output = {
    "routes" : routes,
    "coordinates":coords
}
print(json.dumps(output))