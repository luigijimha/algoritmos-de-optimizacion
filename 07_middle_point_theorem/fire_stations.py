import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from scipy.spatial import Voronoi, voronoi_plot_2d

placeName = 'Oaxaca de Juarez, Mexico'
CSVFireStationFile = './07_middle_point_theorem/fire_stations_oaxaca.csv'

# read location points
df = pd.read_csv(CSVFireStationFile)
fireStationPoints = gpd.points_from_xy(df['longitude'], df['latitude'])

# get Oaxaca city image
OaxacaGraph = ox.graph_from_place(placeName, network_type='drive')
_, ax = ox.plot_graph(OaxacaGraph, show=False, close=False)

# calculate voronoi diagram limits
vor = Voronoi([(p.x, p.y) for p in fireStationPoints])
voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors='red', line_width=5, point_size=20)

# plot the diagram
plt.show()
