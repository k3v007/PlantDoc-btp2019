import json
import os
from glob import glob
from urllib3 import response

import urllib3

http = urllib3.PoolManager()
domain = "http://localhost:8000{}"
PLANTS = {}
admin_email = 'admin@gmail.com'
password = '1234'

r = http.request(
        'POST',
        domain.format('/login'),
        headers={"Content-Type": "application/json"},
        body=json.dumps({
            'email': admin_email,
            "password": password
        }).encode('utf-8')
    )
r = json.loads(r.data)
access_token = r.get('access_token')
refresh_token = r.get('refresh_token')


def httpRequest(method, url, body=None) -> response.HTTPResponse:
    resp = http.request(
               method,
               domain.format(url),
               headers={
                   'Content-Type': 'application/json',
                   'Authorization': f'Bearer {access_token}'
               },
               body=json.dumps(body).encode('utf-8')
           )
    return resp


def registerPlants():
    f_path = "json_data/register_plants.json"
    print("\nRegister Plants: ")
    with open(f_path, 'r') as f:
        plants = json.loads(f.read())
        for plant in plants:
            # print(plant)
            r = httpRequest('POST', '/api/v1/plants', plant)
            print(json.loads(r.data), r.status)


r = httpRequest('GET', '/api/v1/plants')
plants = json.loads(r.data)["plants"]
for plant in plants:
    PLANTS[plant["name"]] = str(plant["id"])


def registerDiseases():
    files = glob("json_data/register_diseases*")
    for fpath in files:
        with open(fpath, 'r') as f:
            plant = os.path.splitext(os.path.split(fpath)[1])[0].split('_')[2]
            print(f"\nRegister {plant.capitalize()} Diseases: ")
            diseases = json.loads(f.read())
            for disease in diseases:
                disease["plant_id"] = PLANTS[plant]
                r = httpRequest('POST', '/api/v1/diseases', disease)
                print(json.loads(r.data), r.status)


registerPlants()
registerDiseases()
