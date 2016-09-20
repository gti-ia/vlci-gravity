import sys
import numpy as np

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

from matplotlib.colors import rgb2hex
import geojson
from geojson import Feature, FeatureCollection, LineString, Polygon


def contour_to_geojson(contour, stroke_width):
    collections = contour.collections
    features = []
    for collection in collections:
        paths = collection.get_paths()
        paths_color = collection.get_edgecolor()
        for path in paths:
            v = path.vertices
            coordinates = []

            for i in range(0, len(v)):  # -1?
                latitude = v[i][0]
                longitude = v[i][1]
                coordinates.append((latitude, longitude))

            geometry = LineString(tuple(coordinates))
            properties = {
                "stroke-width": stroke_width,
                "stroke": rgb2hex(tuple(paths_color[0])[:3]),
            }
            features.append(Feature(geometry=geometry, properties=properties))

    feature_collection = FeatureCollection(features)
    contour_lines_geojson = geojson.dumps(feature_collection, sort_keys=True)
    return contour_lines_geojson


x,y = np.meshgrid(np.arange(-0.43, -0.32, 0.003), np.arange(39.43, 39.5, 0.003))
#x,y = np.meshgrid(np.arange(-0.49, -0.27, 0.003), np.arange(39.42, 39.53, 0.003))

filename = sys.argv[1]

with open(filename, 'r') as f:
    data = " ".join(f.readlines())

data = np.array(eval(data.split("\t")[1]))

n_levels = 20
data = np.log10(data)

min_grav = 0
max_grav = data.max()
incr = (max_grav - min_grav)/(n_levels +1)

levels = np.arange(min_grav, max_grav, incr)

#get the contours
contour = plt.contour(x, y, data, levels)

stroke_width = 2

#matplotlib contour lines to geojson
contour_lines_geojson = contour_to_geojson(contour, stroke_width)


output_file = "output_geojson"
with open(output_file, 'w') as fileout:
    fileout.write(contour_lines_geojson)

