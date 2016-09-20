#!/usr/bin/env python

import sys
import json

import numpy as np
import datetime as dt

if len(sys.argv) == 3:
    min_date = dt.datetime.strptime(sys.argv[1],"%Y%m%d")
    max_date = dt.datetime.strptime(sys.argv[2],"%Y%m%d")
elif len(sys.argv) == 2:
    min_date = dt.datetime(1900,01,01)
    max_date = dt.datetime.strptime(sys.argv[2],"%Y%m%d")
else:
    min_date = dt.datetime(1900,01,01)
    max_date = dt.datetime(2900,01,01)

#x,y = np.meshgrid(np.arange(-0.43,-0.32, 0.003), np.arange(39.43, 39.5, 0.003))
x,y = np.meshgrid(np.arange(-0.49,-0.27, 0.003), np.arange(39.42, 39.53, 0.003))
cumU = np.zeros(x.shape)

for tweet in sys.stdin:
    # Trailing and Leading white space is removed
    tweet = tweet.strip()
    try:
        jsontweet = json.loads(tweet)
        created_at = dt.datetime.strptime(jsontweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
        if jsontweet["coordinates"] != None and (min_date <= created_at <= max_date):
            longitude = float(jsontweet["coordinates"]["coordinates"][0])
            latitude  = float(jsontweet["coordinates"]["coordinates"][1])
        else:
            continue

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
