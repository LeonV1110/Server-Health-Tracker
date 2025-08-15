"""DOCSTRING"""#TODO
import configparser
import time
import datetime
import requests
import pymysql


config = configparser.ConfigParser()
config.read('server-health-tracker/config.ini')

DATABASEUSER = config['DATABASE']['DATABASE_USERNAME']
DATABASEPSW = config['DATABASE']['DATABASE_PASSWORD']
DATABASEHOST = config['DATABASE']['DATABASE_HOST']
DATABASEPORT = config['DATABASE']['DATABASE_PORT']
DATABASENAME = config['DATABASE']['DATABASE_NAME']

API_KEY = config['API']['API_KEY']
API_BASE_URL = config['API']['API_BASE_URL']

INTERVAL = int(config['SETTINGS']['INTERVAL'])

SERVERIDS = config['SERVERID']
SERVERNUMBERS = config['SERVER_NUMBER']


if len(SERVERIDS) != len(SERVERNUMBERS):
    raise ValueError

servers = {}
for key in SERVERNUMBERS:
    servers[SERVERNUMBERS[key]] = f"{API_BASE_URL}{SERVERIDS[key]}/resources"

headers = {
    "Content-Type": "application/json",
    "Accept": "application/vnd.wisp.v1+json",
    "Authorization": f"Bearer {API_KEY}"
}

connection = pymysql.connect(host=DATABASEHOST, port=int(DATABASEPORT),
                             user = DATABASEUSER, password=DATABASEPSW, database=DATABASENAME)



while True:
    for server_num, server_url in servers.items():
        try:
            response = requests.get(server_url, headers=headers, timeout=max(5, INTERVAL/5))
            response.raise_for_status()
            data = response.json()
            memory = data['proc']['memory']['total']
            print(datetime.datetime.now())
            print('memory:', memory)
            cpu = data['proc']['cpu']['total']
            print('cpu:', cpu)
            SQL = "INSERT INTO `stats` (`time`, `server_id`, `cpu`, `memory`) VALUES (%s, %s, %s, %s)" #TODO
            VALUES = (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), server_num, cpu, memory)
            with connection.cursor() as cursor:
                cursor.execute(SQL, VALUES)
            connection.commit()
        except pymysql.OperationalError as e:
            print('Database operation failed:', e)

        except requests.RequestException as e:
            print("Request failed:", e)

    time.sleep(INTERVAL)
