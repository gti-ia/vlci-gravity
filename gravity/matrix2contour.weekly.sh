#! /bin/bash

echo "Start matrix conversion"
python matrix2contour.py26.py -i part-00000 -o gravity.geojson

echo "Finished matrix conversion"

if  $(hadoop fs -test -d "/home/utool_upv/output/latest.weekly.geojson"); then
    hadoop fs -rm /home/utool_upv/output/latest.weekly.geojson
fi

hadoop fs -put gravity.geojson /user/utool_upv/output/latest.weekly.geojson

WEEK=`date +%Y%V`

if  $(hadoop fs -test -d "/home/utool_upv/output/$WEEK.weekly.geojson"); then
    hadoop fs -rm /home/utool_upv/output/$WEEK.weekly.geojson
fi

hadoop fs -put gravity.geojson /user/utool_upv/output/$WEEK.weekly.geojson

echo "Uploaded to HDFS"

