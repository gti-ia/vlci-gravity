#!/usr/bin/env python

import sys
import numpy as np

LAT_CELL = 60
LON_CELL = 50

coord0 = -0.49
coord1 = -0.27
coord2 = 39.42
coord3 = 39.53
lat_range = abs(abs(coord0) - abs(coord1)) / LAT_CELL
lon_range = abs(abs(coord2) - abs(coord3)) / LON_CELL
x, y = np.meshgrid(np.arange(coord0, coord1, lat_range), np.arange(coord2, coord3, lon_range))

# x, y = np.meshgrid(np.arange(-0.43, -0.32, 0.003), np.arange(39.43, 39.5, 0.003))
# x, y = np.meshgrid(np.arange(-0.49, -0.27, 0.003), np.arange(39.42, 39.53, 0.003))

cumU = np.zeros(x.shape)

key = "GRAV"  # default key value

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input we got from mapper
    key, m_str = line.split('\t', 1)

    m = np.array(eval(m_str))

    # accumulate matrix
    try:
        cumU += m
    except ValueError:
        # ignore/discard this line
        continue

print('%s\t%s' % (key, str(cumU.tolist())))
