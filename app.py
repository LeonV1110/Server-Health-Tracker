"""DOCSTRING"""#TODO
import configparser
import time
import requests
import pymysql

config = configparser.ConfigParser()
config.read('config.ini')

DATABASEUSER = config['DATABASE']['DATABASE_USERNAME']
DATABASEPSW = config['DATABASE']['DATABASE_PASSWORD']
DATABASEHOST = config['DATABASE']['DATABASE_HOST']
DATABASEPORT = config['DATABASE']['DATABASE_PORT']
DATABASENAME = config['DATABASE']['DATABASE_NAME']

API_KEY = config['API']['API_KEY']
API_BASE_URL = config['API']['API_BASE_URL']

INTERVAL = config['SETTINGS']['INTERVAL']

SERVERIDS = config['SERVERID']
SERVERNUMBERS = config['SERVER_NUMBER']


if len(SERVERIDS) != len(SERVERNUMBERS):
    raise ValueError

servers = {}
for i in range(len(SERVERNUMBERS)):
    servers[SERVERNUMBERS[i]] = f"{API_BASE_URL}{SERVERIDS[i]}"

headers = {
    "Content-Type": "application/json",
    "Accept": "application/vnd.wisp.v1+json",
    "Authorization": "Bearer APITOKEN"
}

while True:
    for server_url in servers:
        try:
            response = requests.get(server_url, headers=headers, timeout=max(3, INTERVAL/5))
            response.raise_for_status()
            data = response.json()
            print(data)
        except Exception as e:
            print("Request failed:", e)

    time.sleep(INTERVAL)
