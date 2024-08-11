import matplotlib.pyplot as plt
from scipy.spatial import Voronoi
from random import random, randint
import numpy as np

"""
uses voronoi diagrams to find the nearest bus stop to a location
@param {List} bus_stops
@param {Set} start_location
@param {Set} end_location
@return {Set}
"""
def findNearestPoint(bus_stops, location):
    # Extract coordinates of bus stops
    bus_stop_coords = [point for point, _, _, _ in bus_stops]

    # Compute Voronoi diagram
    vor = Voronoi(bus_stop_coords)

    # Find index of the nearest point in the Voronoi diagram
    nearest_index = np.argmin(np.linalg.norm(vor.points - location, axis=1))

    # Return the coordinates of the nearest bus stop
    nearest_bus_stop = bus_stops[nearest_index][0]
    
    return nearest_bus_stop

"""
finds the angle between two vectors
@param {Set} start_point
@param {Set} next_point
@param {Set} destination_point
@return {float}
"""
def findAngleBetweenVector(start_point, next_point, destination_point):
    vec1 = np.array(next_point) - np.array(start_point)
    vec2 = np.array(destination_point) - np.array(start_point)
    angle = np.arccos(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
    return np.degrees(angle)

"""
performs montecarlo simulation to get the mean travel time of certain route
@param {List} bus_stops
@param {Set} start_stop
@param {Set} end_stop
@param {int} total simulations
@return {int}
"""
def montecarloSimulation(bus_stops, start_stop, end_stop, TOTAL_SIMULATIONS=100):
    travel_time = 0
    
    for _ in range(TOTAL_SIMULATIONS):
        current_point = start_stop
        
        # iterate over bus route
        while current_point != end_stop:
            current_index = next(i for i, stop in enumerate(bus_stops) if stop[0] == current_point)
            mean_waiting_time, std_deviation = bus_stops[current_index][2], bus_stops[current_index][3]
            
            # simulate travel time
            travel_time += mean_waiting_time + std_deviation * random() * (1 if randint(0, 1) == 1 else -1)
            
            current_point = bus_stops[current_index][1]
        
    # return travel time mean
    return travel_time / TOTAL_SIMULATIONS

def main(start_location, end_location):
    best_route = []
    min_time = float('inf')
    start_stop = ()
    end_stop = ()

    # select route with smaller travel mean time
    for bus_route in bus_routes:
        start_bus_stop = findNearestPoint(bus_route, start_location)
        end_bus_stop = findNearestPoint(bus_route, end_location)

        print ('start', start_bus_stop, 'end', end_bus_stop)

        route_time = montecarloSimulation(bus_route, start_bus_stop, end_bus_stop)

        print(route_time)

        if route_time < min_time:
            min_time = route_time
            best_route = bus_route
            start_stop = start_bus_stop
            end_stop = end_bus_stop

    # separate and classify points for plotting
    # bus route points
    route_x_coords = []
    route_y_coords = []
    # path to follow points
    suggested_x_coords = []
    suggested_y_coords = []
    suggested_flag = True

    # do while
    current_point = start_stop
    current_index = next(i for i, stop in enumerate(best_route) if stop[0] == current_point)

    suggested_x_coords.append(best_route[current_index][0][0])
    suggested_y_coords.append(best_route[current_index][0][1])

    current_point = best_route[current_index][1]
        
    while current_point != start_stop:
        current_index = next(i for i, stop in enumerate(best_route) if stop[0] == current_point)

        if current_point == end_stop:
            suggested_x_coords.append(best_route[current_index][0][0])
            suggested_y_coords.append(best_route[current_index][0][1])
            suggested_flag = False

        if suggested_flag:
            suggested_x_coords.append(best_route[current_index][0][0])
            suggested_y_coords.append(best_route[current_index][0][1])
        else:
            route_x_coords.append(best_route[current_index][0][0])
            route_y_coords.append(best_route[current_index][0][1])
        
        current_point = best_route[current_index][1]

    # add last point of bus route
    current_index = next(i for i, stop in enumerate(best_route) if stop[0] == current_point)
    route_x_coords.append(best_route[current_index][0][0])
    route_y_coords.append(best_route[current_index][0][1])

    # Plot bus route
    plt.plot(route_x_coords, route_y_coords, marker='o', linestyle='--', color='b')
    plt.plot(suggested_x_coords, suggested_y_coords, marker='o', linestyle='-', color='b')
    plt.scatter(start_location[0], start_location[1], color='r', label='Start')
    plt.scatter(end_location[0], end_location[1], color='g', label='End')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Best Bus Route')
    plt.legend()
    plt.grid(True)
    plt.show()

# list element description
# (bus stop, next bus stop, mean waiting time, standard deviation)
bus_routes = [
    [
        ((5, 1), (4, 1), 4, 1),
        ((4, 1), (3, 2), 4, 2),
        ((3, 2), (3, 3), 4, 1),
        ((3, 3), (2, 4), 4, 1),
        ((2, 4), (1, 5), 5, 2),
        ((1, 5), (1, 6), 5, 2),
        ((1, 6), (2, 5), 5, 1),
        ((2, 5), (3, 4), 5, 1),
        ((3, 4), (4, 4), 4, 1),
        ((4, 4), (5, 3), 4, 2),
        ((5, 3), (6, 2), 4, 2),
        ((6, 2), (5, 1), 4, 1)
    ],
    [
        ((1, 1), (1, 2), 2, 1),
        ((1, 2), (2, 3), 2, 1),
        ((2, 3), (3, 4), 4, 3),
        ((3, 4), (4, 5), 4, 2),
        ((4, 5), (5, 6), 7, 5),
        ((5, 6), (6, 6), 7, 5),
        ((6, 6), (6, 5), 7, 5),
        ((6, 5), (5, 4), 4, 3),
        ((5, 4), (4, 3), 4, 3),
        ((4, 3), (3, 2), 2, 3),
        ((3, 2), (2, 1), 2, 2),
        ((2, 1), (1, 1), 2, 1)
    ],
    [
        ((3, 1), (2, 1), 4, 1),
        ((2, 1), (2, 2), 4, 1),
        ((2, 2), (1, 3), 4, 1),
        ((1, 3), (2, 4), 4, 1),
        ((2, 4), (3, 5), 4, 1),
        ((3, 5), (4, 6), 4, 1),
        ((4, 6), (4, 5), 4, 1),
        ((4, 5), (4, 4), 4, 1),
        ((4, 4), (4, 3), 4, 1),
        ((4, 3), (4, 2), 4, 1),
        ((4, 2), (4, 1), 4, 1),
        ((4, 1), (3, 1), 4, 1)
    ]
]

#start_location = (1, 5)
start_location = (1, 6)
end_location = (6, 1)

main(start_location, end_location)