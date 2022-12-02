
import subprocess
import math
import urllib3
import json
import sys, os, getopt
# To install, do pip install python-dotenv
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

def print_usage():
    print("""
    USAGE: python ckanAPI.py <OPTIONS>

    OPTIONS
    ~~~~~~~
    -h --help : prints help page
    -e --endpoint : specify the endpoint you are trying to reach.  Usage: -e <ENDPOINT>
    -j --json : specify a json to be used as a payload.  Refer to CKAN documentation for
                payload shape.  If no payload is specified, an empty dict is used.  
                Usage: -j <FILENAME>
    -d --dest : specify where it is going to the dev server or not.
                `-d dev` will lead to the CKAN-Dev, `-d prod` will lead to the CKAN-Prod,
                the default is dev
    -o --output : specify which file output should be routed to.  Default is to terminal
    """)

def parse_args(argv):
    endpoint = ''
    destination = ''
    body = ''
    outputFile = ''

    try:
        opts, args = getopt.getopt(argv, "he:j:o:d:", ["help","endpoint=","json=","dest=","output="])
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h','--help'):
            print_usage()
            sys.exit()
        elif opt in ('-e', '--endpoint'):
            endpoint = arg
        elif opt in ('-j', '--json'):
            body = arg
        elif opt in ('-d', '--dest'):
            destination = arg
        elif opt in ('-o', '--output'):
            outputFile = arg
        else:
            print(f"Unknown arg: {opt} {arg}")
            print_usage()
            sys.exit(2)

    return destination, endpoint, body, outputFile

def keyWithTabs(t):
    amount = math.ceil((len(t) + 1)/8)
    tabs = ''
    for i in range(5 - amount):
        tabs += '\t-'
    return t + tabs


def unpackDict(data, indentation):
    for key in data.keys():
        if isinstance(data[key], dict):
            unpackDict(data[key], indentation+1)
        elif isinstance(data[key], list):
            # printSpacing(indentation)
            # print(keyWithTabs(key) + ':')
            unpackList(data[key], indentation+1)
        # else:
            # printSpacing(indentation)
            # print(keyWithTabs(key) + str(data[key]))
    # print('\n', end='')

def unpackList(items, indentation):
    for item in items:
        if isinstance(item, dict):
            unpackDict(item, indentation+1)
        elif isinstance(item, list):
            unpackList(item, indentation+1)
        # else:
            # printSpacing(indentation)
            # print(item, end=", ")

def unpack(data):
    if isinstance(data, dict):
        unpackDict(data, -1)
    elif isinstance(data, list):
        unpackList(data, -1)
    # else:
        # print('ERROR')

# def printSpacing(indentation):
    # for i in range(indentation):
        # print('\t', end='')

def run(destination, endpoint, body, outputFile):
    toDev = (destination == 'dev')

    link = CKAN_URL_DEV if toDev else CKAN_URL_PROD

    API_KEY = API_KEY_CKAN_DEV if toDev else API_KEY_CKAN_PROD
    http = urllib3.PoolManager(headers = {'connection' : 'keep-alive',
                                      'Authorization' : API_KEY,
                                      'Content-Type': 'application/json'})
    payload = dict() if body == '' else json.load(open(body, 'rb'))
    request = http.request('POST',
    url= link + '/api/3/action/' + endpoint,
    body=json.dumps(payload))
    
    if not outputFile == '':
        log = open(outputFile, 'w+')
        old_stdout = sys.stdout
        sys.stdout = log
    unpack(json.loads(request.data.decode('utf-8'))['result'])
    if not outputFile == '':
        sys.stdout = old_stdout
        log.close()

def main(argv):
    destination, endpoint, body, outputFile = parse_args(argv)
    run(destination, endpoint, body, outputFile)

    
if __name__ == '__main__':
    main(sys.argv[1:])
