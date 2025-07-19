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
print(data)