#! /bin/bash

echo "Start matrix conversion"
python matrix2contour.py26.py -i part-00000 -o gravity.geojson

echo "Finished matrix conversion"

exists=`hadoop fs -test -e /user/utool_upv/output/latest.geojson`
echo "Check if latest.geojson exists: $exists"
if  [ $exists==0 ]; then
    echo "latest.geojson exists. Delete it.";
    hadoop fs -rm -f /user/utool_upv/output/latest.geojson
fi

hadoop fs -put gravity.geojson /user/utool_upv/output/latest.geojson

DATE=`date +%Y%m%d%H`

exists=`hadoop fs -test -e /user/utool_upv/output/$DATE.geojson`
echo "Check if $DATE.geojson exists: $exists"
if  [ $exists==0 ]; then
    echo "$DATE.geojson exists. Delete it.";
    hadoop fs -rm -f /user/utool_upv/output/$DATE.geojson
fi

hadoop fs -put gravity.geojson /user/utool_upv/output/$DATE.geojson

echo "Uploaded to HDFS"

