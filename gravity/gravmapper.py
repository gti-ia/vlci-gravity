#!/usr/bin/env python

import sys
from optparse import OptionParser

import gravity

import numpy as np
import datetime as dt

LAT_CELL = 60
LON_CELL = 50

parser = OptionParser()
parser.add_option("-k", "--key", dest="key", default="GRAV",
                  help="Key to produce and send to reducer")
parser.add_option("-i", "--init-date", dest="init_date",
                  help="Min date to process tweets. Format %Y%m%d")
parser.add_option("-e", "--end-date", dest="end_date",
                  help="Max date to process tweets. Format %Y%m%d")
parser.add_option("-d", action="store_true", dest="last24",
                  help="Process tweets from the last 24 hours")
parser.add_option("-w", action="store_true", dest="lastweek",
                  help="Process tweets from the last 7 days")
parser.add_option("-m", action="store_true", dest="lastmonth",
                  help="Process tweets from the last 30 days")
parser.add_option("-y", action="store_true", dest="lastyear",
                  help="Process tweets from the last year")
parser.add_option("-a", action="store_true", dest="all",
                  help="Process tweets from the whole file")

(options, args) = parser.parse_args()
now = dt.datetime.now()

if options.end_date is None and options.init_date is None:
    max_date = now
    if options.all:
        min_date = dt.datetime(1900, 1, 1)
        max_date = dt.datetime(2900, 1, 1)
    elif options.lastyear:
        min_date = now - dt.timedelta(days=365)
    elif options.lastmonth:
        min_date = now - dt.timedelta(days=30)
    elif options.lastweek:
        min_date = now - dt.timedelta(days=7)
    else:  # assume last24
        min_date = now - dt.timedelta(hours=24)
else:
    if options.end_date is None:
        max_date = now
    else:
        max_date = dt.datetime.strptime(options.end_date, "%Y%m%d")
    if options.init_date is None:
        min_date = dt.datetime(1900, 1, 1)
    else:
        min_date = dt.datetime.strptime(options.init_date, "%Y%m%d")

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

for tweet in sys.stdin:
    # Trailing and Leading white space is removed
    tweet = tweet.strip()
    try:
        jsontweet = gravity.loads(tweet)
        created_at = dt.datetime.strptime(jsontweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
        if jsontweet["coordinates"] is not None and (min_date <= created_at <= max_date):
            longitude = float(jsontweet["coordinates"]["coordinates"][0])
            latitude = float(jsontweet["coordinates"]["coordinates"][1])
        else:
            continue

        # m = np.exp(-0.5 * (x - latitude) ** 2 / 0.005 ** 2) * np.exp(-0.5 * (y - longitude) ** 2 / 0.003 ** 2)
        m = np.exp(-0.5 * (x - longitude) ** 2 / 0.005 ** 2) * np.exp(-0.5 * (y - latitude) ** 2 / 0.003 ** 2)

        cumU += m

    except IndexError:
        continue
    except ValueError:
        continue

print("{key}\t{matrix}".format(key=options.key, matrix=str(cumU.tolist())))
