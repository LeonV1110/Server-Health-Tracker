# Server Health Tracker

This app uses the API of PSG's dashboard to track CPU and memory usagage. (hooks into the Wisp Client API, may be usefull outside of PSG too)
It then stores this info into a simple mysql compatable database (The MariaDB PSG offers works).

# How to install

On a box on PSG.
1. Ask PSG to spin up a python instance for you.
2. Head to the file manager and select the git clone button on the top right and fill in `https://github.com/LeonV1110/Server-Health-Tracker.git`
3. Head to the Startup Parameters and fill in `server-health-tracker/app.py` for App py file, and `server-health-tracker/requirements.txt` for Requirements file.
4. Head back to the file manager, go into the server-health-tracker folder and open the config.ini file. see below for config guide.
5. Start the python instance

## Config guide
**Database**
Fill in all the fields, While this should work in an existing database, I recommend seting up a new database. This can be done with the same app, just means they cannot interfere with eachother. I also recommend setting up a dedicated username and psw for this app, restricting access to only the appropiate database.

**Settings**
the interval setting is how many seconds the app will wait before polling the API again. the default 10s is the same as how often squadJS will log the TPS

**API**
To get the API key head to the homepage, here select `Security Control` from the toolbar and create an API key in the top right. Clicking on the key once will reveal it, clicking again will copy.
The base URL should be the same for any server provided you're with psg, if you're with a different provider using wisp, replace the part before `/api` with the link to your pannel.

**ServerID and Server_Number**
Make sure each entry appear in the same order in both SERVERID and SERVER_NUMBER!

All Entries in SERVERID are the ID on the pannel, to get this head to the server on your pannel, and look at the URL. Your serverID will be the last part. `https://control.psg-hosting.com/server/SERVERID`

Server number is simply to make sure it's easy to seperate out the values in the database

Again, make sure each entry appear in the same order in both SERVERID and SERVER_NUMBER!