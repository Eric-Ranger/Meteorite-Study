#Normalize data and put it into new databases with multiple tables
import json
import sqlite3

conn = sqlite3.connect('dw_meteorite.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Landings')
cur.execute('DROP TABLE IF EXISTS Nametype')
cur.execute('DROP TABLE IF EXISTS Class')
cur.execute('DROP TABLE IF EXISTS FallStatus')
cur.execute('DROP TABLE IF EXISTS Country')

cur.execute('''CREATE TABLE IF NOT EXISTS Landings
            (id INTEGER PRIMARY KEY, Name TEXT UNIQUE, type_id INTEGER,
             class_id INTEGER, mass_grams REAL, fall_id INTEGER,
             year NUMERIC, reclat REAL, reclong REAL, country_id INTEGER)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Nametype
            (id INTEGER PRIMARY KEY, nametype TEXT UNIQUE)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Class
            (id INTEGER PRIMARY KEY, recclass TEXT UNIQUE)''')

cur.execute('''CREATE TABLE IF NOT EXISTS FallStatus
            (id INTEGER PRIMARY KEY, fall TEXT UNIQUE)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Country
            (id INTEGER PRIMARY KEY, country TEXT UNIQUE)''')

conn_2 = sqlite3.connect('file:location_data.sqlite?mode=ro', uri = True)
cur_2 = conn_2.cursor()

def get_country(latitue, longitude):
    cur_2.execute('''SELECT json FROM location
                WHERE lat = ? AND lng = ?''', (latitue, longitude))

    row_2 = cur_2.fetchone()
    if row_2 is None: return None

    data = str(row_2[0].decode())
    js = json.loads(str(data))

    if js['status'] == 'ZERO_RESULTS' :
        print('==== Failure To Retrieve ====')
        return None

    i = 0
    while i < len(js['results'][0]['address_components']):

        value = js['results'][0]['address_components'][i]['types'][0]
        if value == "country":
            return(js['results'][0]['address_components'][i]['long_name'])
        i = i + 1
    return None

conn_1 = sqlite3.connect('file:raw_meteorite.sqlite?mode=ro', uri=True)
cur_1 = conn_1.cursor()

cur_1.execute('SELECT * FROM Landings')

for row in cur_1:
    name = row[1]
    nametype = row[2]
    recclass = row[3]
    mass = row[4]
    fall = row[5]
    year = row[6]
    reclat = row[7]
    reclong = row[8]

    if reclat == 0 and reclong == 0:
        reclat = None
        reclong = None
        country = None
    else:
        country = get_country(reclat,reclong)

    cur.execute('INSERT OR IGNORE INTO Nametype (nametype) VALUES (?)',(nametype,))
    conn.commit()
    cur.execute('SELECT id FROM Nametype WHERE nametype = ? LIMIT 1',(nametype,))
    try:
        row = cur.fetchone()
        type_id = row[0]
    except:
        print('Could not retrieve nametype id', nametype)
        break

    cur.execute('INSERT OR IGNORE INTO Class (recclass) VALUES (?)',(recclass,))
    conn.commit()
    cur.execute('SELECT id FROM Class WHERE recclass = ? LIMIT 1',(recclass,))
    try:
        row = cur.fetchone()
        class_id = row[0]
    except:
        print('Could not retrieve recclass id', recclass)
        break

    cur.execute('INSERT OR IGNORE INTO FallStatus (fall) VALUES (?)',(fall,))
    conn.commit()
    cur.execute('SELECT id FROM FallStatus WHERE fall = ? LIMIT 1',(fall,))
    try:
        row = cur.fetchone()
        fall_id = row[0]
    except:
        print('Could not retrieve fall id', fall)
        break

    if country is None:
        country_id = None
    else:
        cur.execute('INSERT OR IGNORE INTO Country (country) VALUES (?)',(country,))
        conn.commit()
        cur.execute('SELECT id FROM Country WHERE country = ? LIMIT 1',(country,))
        try:
            row = cur.fetchone()
            country_id = row[0]
        except:
            print('Could not retrieve country id', counrty)
            break

    cur.execute('''INSERT OR IGNORE INTO Landings(name, type_id, class_id,
                    mass_grams, fall_id, year, reclat, reclong, country_id)
                VALUES (?,?,?,?,?,?,?,?,?)''',
                (name, type_id, class_id, mass, fall_id, year, reclat, reclong, country_id))
    conn.commit()
