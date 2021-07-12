import urllib.request, urllib.parse, urllib.error
import http
import sqlite3
import json
import time
import ssl
import sys

conn = sqlite3.connect('geometeor.sqlite')
cur = conn.cursor()

#load raw data and create database for it
cur.execute('''CREATE TABLE IF NOT EXISTS Landings(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT NOT NULL UNIQUE,
    nametype TEXT,
    recclass TEXT,
    mass_grams REAL,
    fall TEXT,
    year NUMERIC,
    reclat REAL,
    reclong REAL
)''')

def parseyear(yr):
    if yr is None:
        tyear = None
    else:
        tyear = yr[:4]

    return tyear

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://data.nasa.gov/api/views/gh4g-9sfh/rows.json'

open = urllib.request.urlopen(url)
data = open.read().decode()

try:
    js = json.loads(data)
except:
    js = None

for item in js['data']:
    #id = item.get('id',None)
    #if id is None : continue

    name = item[8]
    if name is None: continue
    name = name.strip().lower()

    nametype = item[10]
    nametype = nametype.strip().lower()

    recclass = item[11]
    recclass = recclass.strip().lower()

    mass_grams = item[12]

    fall = item[13]
    fall = fall.strip().lower()

    year = item[14]
    year = parseyear(year)

    reclat = item[15]
    reclong = item[16]

    print(name, nametype, recclass, mass_grams, fall, year, reclat, reclong)

    cur.execute('''
                INSERT OR IGNORE INTO Landings (name, nametype, recclass, mass_grams, fall, year, reclat, reclong)
                VALUES(?,?,?,?,?,?,?,?)''', (name, nametype, recclass, mass_grams, fall, year, reclat, reclong))
    conn.commit()
