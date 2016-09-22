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

### Running with Hadoop

The mapper file reads the data from the stdin and produces a matrix with the gravitatory potential in each cell.
It has the following use:

```
python gravmapper.py -h
Usage: gravmapper.py [options]

Options:
  -h, --help            show this help message and exit
  -k KEY, --key=KEY     Key to produce and send to reducer
  -i INIT_DATE, --init-date=INIT_DATE
                        Min date to process tweets. Format %Y%m%d
  -e END_DATE, --end-date=END_DATE
                        Max date to process tweets. Format %Y%m%d
  -d                    Process tweets from the last 24 hours
  -w                    Process tweets from the last 7 days
  -m                    Process tweets from the last 30 days
  -y                    Process tweets from the last year
  -a                    Process tweets from the whole file
```

The reducer file combines all the produced matrix into an accumulated one.

Finally the matrix2contour file reads the matrix file and writes a geoJSON file that represents the matrix as a contour chart.
It has the following use:

```
python matrix2contour.py26.py -h
Usage: matrix2contour.py26.py [options]

Options:
  -h, --help            show this help message and exit
  -i FILE, --input=FILE
                        an input file with a numpy matrix preceded by a key
                        and a \t.
  -o FILE, --output=FILE
                        an output file.
```

### Running without Hadoop

In the case you want to test the algorithm with a small set of data (see json/examples folder) you can run:

```bash
cat json/example/example_input_tweets.txt | json/grav.py | sort -k1,1 | json/gravreducer.py
```

