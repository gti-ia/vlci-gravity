import json
import os

import requests

auth_url = "https://auth-pre.iotplatform.telefonica.com:15001/v3/auth/tokens"

cb_url = "https://cb-pre.iotplatform.telefonica.com:10027/"

headers = {'Fiware-Service': 'sc_vlci',
           'Fiware-ServicePath': '/utool',
           'X-Auth-Token': None}

def create_entity(entity, username, password):
    token = gettoken(username, password)
    headers['X-Auth-Token'] = token
    
    payload = {'geojson': {'type': 'GeoJson',
                           'value': {}
                          },
               'id': entity,
               'type': 'GeoJson'}

    res = requests.post(cb_url+"v2/entities", headers=headers, json=payload)
    return res.status_code, res.text


def get_entity(entity, username, password):
    token = gettoken(username, password)
    headers['X-Auth-Token'] = token
    res = requests.get(cb_url+"v2/entities/{0}/attrs/geojson".format(entity), headers=headers)
    return res.text


def gettoken(username, password):
    auth = {'auth': {'identity': {'methods': ['password'],
                                  'password': {'user': {'domain': {'name': 'sc_vlci'},
                                                        'name': username,
                                                        'password': password}}},
                     'scope': {'project': {'domain': {'name': 'sc_vlci'}, 'name': '/utool'}}}}
    res = requests.post(auth_url, json=auth)
    return res.headers["X-Subject-Token"]


def put_new_geojson(entity, username, password):
    token = gettoken(username, password)
    headers['X-Auth-Token'] = token

    os.system("hadoop fs -get /user/utool_upv/output/latest.geojson gravity.geojson")
    with open("gravity.geojson") as file:
        geojson = json.load(file)

    payload = {'type': 'GeoJson', 'value': geojson}

    result = requests.put(cb_url+"v2/entities/{entity}/attrs/geojson".format(entity=entity), headers=headers, json=payload)
    print(result.status_code, result.text)

if __name__ == "__main__":
    put_new_geojson("vlcgravity", "", "")
