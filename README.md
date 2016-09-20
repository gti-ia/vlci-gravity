# VLCi potential gravitatory algorithm

Potential gravitatory algorithm.

Prepared for Apache Hadoop.

LICENSE: BSD


## Getting up and running

### Basics


The steps below will get you up and running with a local development environment. We assume you have the following installed:

* pip
* numpy
* matplotlib
* geojson

First make sure to create and activate a virtualenv, then open a terminal at the project root and install the requirements for local development::

```bash
$ pip install -r requirements.txt
```

### Running without Hadoop

In the case you want to test the algorithm with a small set of data (see json/examples folder) you can run:

```bash
cat json/example_input_tweets.txt | json/grav.py | sort -k1,1 | json/gravreducer.py
```

