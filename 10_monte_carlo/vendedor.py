from random import shuffle
from math import sqrt

def randomizeRoute():
    route = CITIES.copy()
    shuffle(route)
    route.append(("Origin", (0, 0)))
    return route

def calculateRouteDistance(route):
    x1, y1 = (0, 0)
    distance = 0
    for _, coords in route:
        x2, y2 = coords
        distance += sqrt((x1-x2)**2 + (y1-y2)**2)
        x1, y1 = (x2, y2)

    return distance

def main():
    minDistance = float('inf')
    optimalRoute = []
    for _ in range(SIMULATIONS):
        route = randomizeRoute()
        newDistance = calculateRouteDistance(route)
        if newDistance < minDistance:
            minDistance = newDistance
            optimalRoute = route

    print('route found: ', end="Origin ")
    for place, _ in optimalRoute:
        print("-> ", end=place)


CITIES = [
    ("Coruscant", (2, 4)),
    ("Mos Eisley", (5, 10)),
    ("Ciudad nublada", (7, 6)),
    ("Theed", (12, 3)),
    ("Otoh Gunga", (9, 1))
]

SIMULATIONS = 100000

main()