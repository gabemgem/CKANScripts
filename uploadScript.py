import requests
import urllib3
import json
import re
import os
from dotenv import load_dotenv
import sys

load_dotenv()

API_KEY_CKAN_DEV=os.getenv('API_KEY_DEV_GOV')
API_KEY_CKAN_PROD=os.getenv('API_KEY_CKAN_PROD')

GROUP_ID_CKAN_DEV=os.getenv('GROUP_ID_CKAN_DEV')
GROUP_ID_CKAN_PROD=os.getenv('GROUP_ID_CKAN_PROD')

ORG_CKAN_DEV=os.getenv('ORG_CKAN_DEV')
ORG_CKAN_PROD=os.getenv('ORG_CKAN_PROD')

CKAN_URL_DEV=os.getenv('CKAN_URL_DEV')
CKAN_URL_PROD=os.getenv('CKAN_URL_PROD')


jsonFile=

#Controls ternary assignments throughout the script
toDev = True

###########################################################################
Group = []
if toDev:
    Group.append({"id": GROUP_ID_CKAN_DEV})
else:
    Group.append({"id": GROUP_ID_CKAN_PROD})

link = CKAN_URL_DEV if toDev else CKAN_URL_PROD

API_KEY = API_KEY_CKAN_DEV if toDev else API_KEY_CKAN_PROD

ORG_ID = ORG_CKAN_DEV if toDev else ORG_CKAN_PROD

GROUP_ID = GROUP_ID_CKAN_DEV if toDev else GROUP_ID_CKAN_PROD


http = urllib3.PoolManager(headers = {'connection' : 'keep-alive',
                                      'Authorization' : API_KEY,
                                      'Content-Type': 'application/json'})

uploadedTags = []
vocabIDs = dict()

"""
We no longer use tags, but this code might be helpful at some point
in the future.
"""
# def initializeTags():
#     vocabularies = []
#     for vocab in vocabularies:
#         request = http.request(method='POST', 
#         url= link + '/api/3/action/vocabulary_create',
#         body=json.dumps({'name' : vocab}))
    
#     # Get ID's of vocabularies for adding tags later
#     request = http.request(method='POST', 
#     url= link + '/api/3/action/vocabulary_list')
#     for i in range(len(json.loads(request.data.decode('utf-8'))['result'])):
#         vocabIDs[vocabularies[i]] = json.loads(request.data.decode('utf-8'))['result'][i]['id']
                


# Uploads a resource to a dataset after constructing a resource dictionary.
# See http://docs.ckan.org/en/2.9/api/index.html#ckan.logic.action.create.resource_create for resource dictionary formatting
# Does NOT make a new dataset, and thus should not be used for making datasets.
def resourceUpload(resourceDict):
    request = http.request(method='POST', 
    url= link + '/api/3/action/resource_create',
    body=json.dumps(resourceDict),
    headers={'Authorization' : API_KEY,
    'Content-Type': 'application/json'})


def upload(dataset):
    uploadDataset = dict()
    # Causes errors if extras uses names that are also used in the 
    # CKAN API call.  Also helps skip any fields that are handled explicitly elsewhere
    # Basically, anything in this list will not go into the "extras" field and needs
    # to be handled separately.
    originalFields = ['name', 
                      'title', 
                      'private', 
                      'author',
                      'author_email',
                      'maintainer', 
                      'maintainer_email',
                      'license_id',
                      'notes',
                      'url',
                      'version',
                      'state',
                      'type',
                      'resources',
                      'tags',
                      'extras',
                      'relationships_as_object',
                      'relationships_as_subject',
                      'groups',
                      'owner_org'
                      ]
    extraKeys = filter((lambda k: not k in originalFields), dataset.keys())

    ## Need to be specifically handled in order to not cause duplicate name conficts/for formatting

    uploadDataset['name'] = dataset['name'] # For internals
    uploadDataset['title'] = dataset['title'] # For display
    uploadDataset['notes'] = '' if not 'notes' in dataset.keys() else dataset['notes']
    uploadDataset['version'] = '' if not 'version' in dataset.keys() else dataset['version']
    uploadDataset['private'] = False

    # Grab remaining fields that don't fit well into CKAN and upload current value
    uploadDataset['extras'] = list()
    for key in extraKeys:
        if isinstance(dataset[key], list):
            uploadDataset['extras'].append({'key' : key, 'value' : ':~:'.join(dataset[key])})
        else:
            uploadDataset['extras'].append({'key' : key, 'value' : dataset[key]})

    #Groups are not necessary, but an owner organization currently is
    uploadDataset['owner_org'] = ORG_ID
    uploadDataset['groups'] = [{'id' : GROUP_ID}]

    request = http.request(method='POST', 
                           url= link + '/api/3/action/package_create',
                           body=json.dumps(uploadDataset))

    # Confirm success, then read response to get dataset ID
    if not json.loads(request.data.decode('utf-8'))['success']:
        print("Dataset did not upload", dataset["name"])
        print(json.loads(request.data.decode('utf-8')))
    else:
        resourcesUploaded = False
        while not resourcesUploaded:
            try:
                # getDatasetResources(dataset, json.loads(request.data.decode('utf-8'))['result']['id'])
                resourcesUploaded = True
            except:
                resourcesUploaded = False
    
        

with open(jsonFile) as jsonData:
    DatasetDict = json.load(jsonData)

#upload each individually
# uploaded = False 
# while not uploaded:
#     try:
#         initializeTags()
#         uploaded = True
#     except:
#         uploaded = False

upload_count = 0
uploaded = False 
print(f"Trying to upload {len(DatasetDict)} datasets.")
for dataset in DatasetDict:
    while not uploaded:
        try:
            upload(dataset)
            uploaded = True
        except:
            uploaded = False
    uploaded = False
    upload_count += 1
    if upload_count % 10 == 0:
        print(f"Uploaded {upload_count} datasets.")

print(f"Uploaded {upload_count} datasets.")
