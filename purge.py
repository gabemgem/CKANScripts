import requests
import urllib3
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY_CKAN_DEV=os.getenv('API_KEY_DEV_GOV')
API_KEY_CKAN_PROD=os.getenv('API_KEY_CKAN_PROD')

GROUP_ID_CKAN_DEV=os.getenv('GROUP_ID_CKAN_DEV')
GROUP_ID_CKAN_PROD=os.getenv('GROUP_ID_CKAN_PROD')

ORG_CKAN_DEV=os.getenv('ORG_CKAN_DEV')
ORG_CKAN_PROD=os.getenv('ORG_CKAN_PROD')

CKAN_URL_DEV=os.getenv('CKAN_URL_DEV')
CKAN_URL_PROD=os.getenv('CKAN_URL_PROD')

## Please note that this script does not purge users but it *does* currently purge tags and vocabularies.  
## Tags are currently hardcoded into endpoints so they will need to be updated.

#Controls ternary assignments throughout the script
toDev = True

http = urllib3.PoolManager()

link = CKAN_URL_DEV if toDev else CKAN_URL_PROD

API_KEY = API_KEY_CKAN_DEV if toDev else API_KEY_CKAN_PROD



request = http.request(method='POST', 
    url= link + '/api/3/action/package_list',
    headers={'Authorization' : API_KEY,
             'Content-Type': 'application/json'})


purged = False
for package in json.loads(request.data.decode('utf-8'))['result']:
    while not purged:
        try:
            http.request(method='POST', 
                        url= link + '/api/3/action/package_delete',
                        body=json.dumps({'id': package}),
                        headers={'Authorization' : API_KEY,
                                'Content-Type': 'application/json'})
            purged = True
        except:
            purged = False
    purged = False

request = http.request(method='POST', 
                       url= link + '/api/3/action/vocabulary_list',
                       headers={'Authorization' : API_KEY,
                                'Content-Type': 'application/json'})

purgedvocab = False
for vocab in json.loads(request.data.decode('utf-8'))['result']:
    #Empty Vocabs before deleting them tags first
    purgedTag = False
    for tag in vocab['tags']:
        while not purgedTag:
            try:
                request = http.request(method='POST', 
                                    url= link + '/api/3/action/tag_delete',
                                    body=json.dumps({'id': tag['id'], 'vocabulary_id': vocab['id']}),
                                    headers={'Authorization' : API_KEY,
                                                'Content-Type': 'application/json'})
                purgedTag = True
            except:
                purgedTag = False
        purgedTag = False
    while not purgedvocab:
        try:
            request = http.request(method='POST', 
            url= link + '/api/3/action/vocabulary_delete',
            body=json.dumps({'id' : vocab['id']}),
            headers={'Authorization' : API_KEY,
            'Content-Type': 'application/json'})
            purgedvocab = True
        except:
            purgedvocab = False
    purgedvocab = False
