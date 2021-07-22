#create and fill database with lat lng json file from google api
import urllib.request, urllib.parse, urllib.error
import sqlite3
import json
import ssl

conn = sqlite3.connect('location_data.sqlite')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS location(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                lat REAL NOT NULL,
                lng REAL NOT NULL,
                json TEXT,
              CONSTRAINT unq_lat_lng UNIQUE (lat,lng) ON CONFLICT IGNORE
)''')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

google_api_key = "put key here"

def load_database(latitue, longitude):
    base = "https://maps.googleapis.com/maps/api/geocode/json?"
    field = "latlng="
    latlng = str(latitue) + "," + str(longitude)
    api_key = "&key=" + google_api_key
    api_url = base +  field + latlng + api_key
    open = urllib.request.urlopen(api_url, context=ctx)
    data = open.read().decode()

    try:
        js = json.loads(data)
    except:
        js = None

    if "error_message" in js.keys():
        print(js["error_message"],js["status"])
        exit()

    cur.execute('''INSERT OR IGNORE INTO location (lat, lng, json)
                    VALUES(?,?,?)''', (latitue, longitude, memoryview(data.encode())))
    conn.commit()

conn2 = sqlite3.connect('raw_meteorite.sqlite')
cur2 = conn2.cursor()

cur2.execute('''SELECT reclat, reclong FROM landings ''')
for row in cur2:

    cur.execute('''SELECT lat, lng FROM location
                    WHERE lat = ? AND lng = ?''',(row[0],row[1]))
    try:
        row1 = cur.fetchone()
        if row1 is not None: continue
    except:
        row1 = None

    if row[0] is None or row[1] is None: continue
    if row[0] < -90 or row[0] > 90: continue
    if row[1] < -180 or row[1] > 180: continue

    print(row[0],row[1])
    lat = row[0]
    lng = row[1]
    load_database(lat, lng)
