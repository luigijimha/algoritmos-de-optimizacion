import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from scipy.spatial import Voronoi, voronoi_plot_2d

place_name = 'Oaxaca de Juarez, Mexico'
csv_file = './middle_point_theorem/fire_stations_oaxaca.csv'

# read location points
df = pd.read_csv(csv_file)
geometry = gpd.points_from_xy(df['longitude'], df['latitude'])

# get Oaxaca city city image
G = ox.graph_from_place(place_name, network_type='drive')
fig, ax = ox.plot_graph(G, show=False, close=False)

# calculate voronoi diagram limits
vor = Voronoi([(p.x, p.y) for p in geometry])
voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors='red', line_width=5, point_size=20)

# plot the diagram
plt.show()
