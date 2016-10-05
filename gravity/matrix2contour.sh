#! /bin/bash

echo "Start matrix conversion"
python matrix2contour.py26.py -i part-00000 -o gravity.geojson

echo "Finished matrix conversion"

if  $(hadoop fs -test -d "/home/utool_upv/output/latest.geojson"); then
    hadoop fs -rm /home/utool_upv/output/latest.geojson
fi

hadoop fs -put gravity.geojson /user/utool_upv/output/latest.geojson

DATE=`date +%Y%m%d%H`

if  $(hadoop fs -test -d "/home/utool_upv/output/$DATE.geojson"); then
    hadoop fs -rm /home/utool_upv/output/$DATE.geojson
fi

hadoop fs -put gravity.geojson /user/utool_upv/output/$DATE.geojson

echo "Uploaded to HDFS"

