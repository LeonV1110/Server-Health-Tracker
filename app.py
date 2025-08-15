"""DOCSTRING"""#TODO
import configparser
import time
import logging
from logging.handlers import TimedRotatingFileHandler
import sys
import datetime
import requests
import pymysql

# Import configs
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

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


file_handler = TimedRotatingFileHandler(
    "server-health-tracker/logs/app.log",           # Base log file name
    when="midnight",                                # Rotate at midnight
    interval=1,                                     # Every 1 day
    backupCount=7,                                  # Keep last 7 days
    encoding="utf-8"                                # Avoid encoding issues
)
file_handler.setLevel(logging.ERROR)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

logger.addHandler(file_handler)
logger.addHandler(console_handler)



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
def connectDB():
    return pymysql.connect(host=DATABASEHOST, port=int(DATABASEPORT),
                             user = DATABASEUSER, password=DATABASEPSW, database=DATABASENAME)


def main():
    connection = None
    while True:
        #reconnect to DB if needed
        try: 
            if connection is None or not connection.open:
                logger.warning("Lost database connection. Reconnecting...")
                connection = connectDB()
                logger.info("Database reconnected.")
        except pymysql.OperationalError as e:
            logger.error(f'Reconnecting failed: {e}')
        
        for server_num, server_url in servers.items():
            try:
                logger.info(f'Polling server {server_num}')
                response = requests.get(server_url, headers=headers, timeout=max(5, INTERVAL/5))
                response.raise_for_status()

                data = response.json()
                logger.debug('_____________________')
                logger.debug(data)
                logger.debug('_____________________')
                if data['status'] != 0:
                    memory = data['proc']['memory']['total']
                    cpu = data['proc']['cpu']['total']
                    logger.info(datetime.datetime.now())
                    logger.info(f'memory: {memory}')
                    logger.info(f'cpu: {cpu}')

                    SQL = "INSERT INTO `stats` (`time`, `server_id`, `cpu`, `memory`) VALUES (%s, %s, %s, %s)" #TODO
                    VALUES = (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), server_num, cpu, memory)
                    with connection.cursor() as cursor:
                        cursor.execute(SQL, VALUES)
                    connection.commit()
                else:
                    logger.info(f'Server {server_num} is not running')
            except pymysql.OperationalError as e:
                logger.error(f'Database operation failed: {e}')

            except requests.RequestException as e:
                logger.error(f"Request failed: {e}")
            
        logger.info(f'Waiting {INTERVAL}s')
        time.sleep(INTERVAL)


if __name__ == "__main__":
    try: 
        main()
    except Exception as e:
        logger.error(f"Catastrofic error: {e}", exc_info=True)
