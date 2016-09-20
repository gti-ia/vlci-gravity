#!/usr/bin/env python

import sys
import csv

import numpy as np

x,y = np.meshgrid(np.arange(-0.43,-0.32, 0.003), np.arange(39.43, 39.5, 0.003))
cumU = np.zeros(x.shape)

for tweet in sys.stdin:
    # Trailing and Leading white space is removed
    tweet = tweet.strip()
    try:
        csvtweet = csv.reader([tweet])
        longitude = float(list(csvtweet)[0][-2:-1][0].strip())
        csvtweet = csv.reader([tweet])
        latitude  = float(list(csvtweet)[0][-1:][0].strip())

        #m = np.exp(-0.5*(x - latitude)**2/0.005**2) * np.exp(-0.5*(y - longitude)**2/0.003**2) 
        m = np.exp(-0.5*(x - longitude)**2/0.005**2) * np.exp(-0.5*(y - latitude)**2/0.003**2) 

        #print("VLC\t{matrix}".format(matrix=m.tostring()))
        #print("VLC\t{lat}\t{lon}\t{matrix}".format(lat=latitude, lon=longitude, matrix=str(m.tolist())))

        cumU += m

    except IndexError:
        continue
    except ValueError:
        continue

print("VLC\t{matrix}".format(matrix=str(cumU.tolist())))
