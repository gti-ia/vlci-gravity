#!/usr/bin/env python

from operator import itemgetter
import sys
import numpy as np

#x,y = np.meshgrid(np.arange(-0.43,-0.32, 0.003), np.arange(39.43, 39.5, 0.003))
x,y = np.meshgrid(np.arange(-0.49,-0.27, 0.003), np.arange(39.42, 39.53, 0.003))

cumU = np.zeros(x.shape)

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input we got from mapper.py
    m_str = line.split('\t', 1)[1]

    m = np.array(eval(m_str))

    # convert count (currently a string) to int
    try:
        cumU += m
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue

    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer

print '%s\t%s' % ("VLC", str(cumU.tolist()))

