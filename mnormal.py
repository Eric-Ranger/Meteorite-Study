import sqlite3

conn = sqlite3.connect('nmeteorite.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Landings')
cur.execute('DROP TABLE IF EXISTS Nametype')
cur.execute('DROP TABLE IF EXISTS Class')
cur.execute('DROP TABLE IF EXISTS FallStatus')

cur.execute('''CREATE TABLE IF NOT EXISTS Landings
            (id INTEGER PRIMARY KEY, Name TEXT UNIQUE, type_id INTEGER,
             class_id INTEGER, mass_grams REAL, fall_id INTEGER,
             year NUMERIC, reclat REAL, reclong REAL)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Nametype
            (id INTEGER PRIMARY KEY, nametype TEXT UNIQUE)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Class
            (id INTEGER PRIMARY KEY, recclass TEXT UNIQUE)''')

cur.execute('''CREATE TABLE IF NOT EXISTS FallStatus
            (id INTEGER PRIMARY KEY, fall TEXT UNIQUE)''')

conn_1 = sqlite3.connect('file:geometeor.sqlite?mode=ro', uri=True)
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
        print('Could not retrieve recclass id', nametype)
        break

    cur.execute('INSERT OR IGNORE INTO FallStatus (fall) VALUES (?)',(fall,))
    conn.commit()
    cur.execute('SELECT id FROM FallStatus WHERE fall = ? LIMIT 1',(fall,))
    try:
        row = cur.fetchone()
        fall_id = row[0]
    except:
        print('Could not retrieve fall id', nametype)
        break

    cur.execute('''INSERT OR IGNORE INTO Landings(name, type_id, class_id,
                    mass_grams, fall_id, year, reclat, reclong)
                VALUES (?,?,?,?,?,?,?,?)''',
                (name, type_id, class_id, mass, fall_id, year, reclat, reclong))
    conn.commit()
