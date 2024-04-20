import osmnx as ox
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
from math import sqrt
from itertools import combinations

placeName = 'Oaxaca de Juarez, Mexico'

# input array
locations = [
    (17.069865,-96.733953),
    (17.070144,-96.726420),
    (17.069444,-96.727778),
    (17.045278,-96.767833),
    (17.486667,-96.875000)
]

# find all possible location combination points
locationCombinations = combinations(locations, 3)

# find the combination with the longest distance between points
longestDistance = 0
c = ()

for combination in locationCombinations:
    distance = 0
    for i in range(-1, len(combination) -1):
        A = combination[i]
        B = combination[i+1]
        d = sqrt(((A[0] - B[0])**2) + ((A[1] - B[1])**2))
        distance += d

    if distance > longestDistance:
        longestDistance = distance
        points = combination

# get Oaxaca city image
OaxacaGraph = ox.graph_from_place(placeName, network_type='drive')
_, ax = ox.plot_graph(OaxacaGraph, show=False, close=False)

# calculate voronoi diagram limits
vor = Voronoi([(p[0], p[1]) for p in points])
voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors='red', line_width=5, point_size=20)

# plot the diagram
plt.show()