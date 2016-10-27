#! /bin/bash

if  $(hadoop fs -test -d "/user/utool_upv/output_6h/mapreduce"); then
    hadoop fs -rm -r /user/utool_upv/output_6h/mapreduce
fi

