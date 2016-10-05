#! /bin/bash

if  $(hadoop fs -test -d "/user/utool_upv/output_week/mapreduce"); then
    hadoop fs -rm -r /user/utool_upv/output_week/mapreduce
fi


