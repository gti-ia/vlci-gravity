#! /bin/bash

echo "Start matrix conversion"
python matrix2contour.py26.py -i part-00000 -o gravity.geojson

echo "Finished matrix conversion"

exists=`hadoop fs -test -e /user/utool_upv/output/latest.weekly.geojson`
echo "Check if latest.weekly.geojson exists: $exists"
if  [ $exists==0 ]; then
    echo "latest.weekly.geojson exists. Delete it.";
    hadoop fs -rm -f /user/utool_upv/output/latest.weekly.geojson
fi

hadoop fs -put gravity.geojson /user/utool_upv/output/latest.weekly.geojson

WEEK=`date +%Y%V`

exists=`hadoop fs -test -e /user/utool_upv/output/$WEEK.weekly.geojson`
echo "Check if $WEEK.weekly.geojson exists: $exists"
if  [ $exists==0 ]; then
    echo "$WEEK.weekly.geojson exists. Delete it.";
    hadoop fs -rm -f /user/utool_upv/output/$WEEK.weekly.geojson
fi

hadoop fs -put gravity.geojson /user/utool_upv/output/$WEEK.weekly.geojson

echo "Uploaded to HDFS"

