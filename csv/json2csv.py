import json
import csv
from io import StringIO
import codecs
import argparse

from tqdm import tqdm

parser = argparse.ArgumentParser(description='Convert tweets from json to csv format.')
parser.add_argument('--source', dest="source", help='source file in json format')
parser.add_argument('--output', dest='output', help='output file')

args = parser.parse_args()

keys = ['id', 'lang', 'in_reply_to_screen_name', 'in_reply_to_status_id', 'in_reply_to_user_id',
        'retweet_count', 'retweeted', 'favorite_count']
headers = keys + ["country", "retweeted_status", "user_id", "screen_name", "longitude", "latitude", "text"]

buf = []
numlines=0

with open(args.source,'r', encoding='utf-8') as source:
    with open(args.output, 'a') as f:
        output = csv.writer(f)
        output.writerow(headers)
    for line in tqdm(source):
            numlines += 1
            #if numlines > 2000:
            #    break
            #else:
            json_tweet = json.loads(line)
            tweet = dict()
            for key in keys:
                tweet[key] = json_tweet[key]
            tweet['country'] = json_tweet['place']['country'] if json_tweet['place'] != None else None
            tweet['retweeted_status'] = json_tweet['retweeted_status']['id'] if 'retweeted_status' in json_tweet else None
            tweet['user_id'] = json_tweet['user']['id'] if json_tweet['user'] != None else None
            tweet['screen_name'] = json_tweet['user']['screen_name'] if json_tweet['user'] != None else None
            tweet['longitude'] = json_tweet['coordinates']['coordinates'][0] if json_tweet['coordinates'] != None else None
            tweet['latitude'] = json_tweet['coordinates']['coordinates'][1] if json_tweet['coordinates'] != None else None

            tweet['text'] = json_tweet["text"].replace('"',"'").replace("\n"," ").strip()

            buf.append([tweet[k] for k in headers])
            if len(buf) > 1000:
                with open(args.output, 'a', encoding='utf-8') as f:
                    output = csv.writer(f)
                    output.writerows(buf)
                buf = []
