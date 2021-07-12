#create json file of geodata for map visual
#includes lat, long, size, name
import sqlite3
import json
import codecs

conn = sqlite3.connect('nmeteorite.sqlite')
cur = conn.cursor()

cur.execute('''SELECT name, mass_grams, reclat, reclong, year, fall, recclass
            FROM Landings, Class, FallStatus
            WHERE Landings.class_id = Class.id
            AND Landings.fall_id = FallStatus.id''')

data = {}
data['landings'] = []

count = 0
for row in cur:
    name = row[0]
    name = name.replace("'","")
    mass_grams = row[1]
    reclat = row[2]
    reclong = row[3]
    year = row[4]
    fall = row[5]
    recclass = row[6]

    #if reclat is None or reclong is None : continue
    if mass_grams is None: mass_grams = 0

    count = count + 1

    data['landings'].append({
    'name': name,
    'mass_grams' : mass_grams,
    'reclat' : reclat,
    'reclong' : reclong,
    'year' : year,
    'fall' : fall,
    'recclass' : recclass
    })

fh = codecs.open('mmap.json','w',"utf-8")
json.dump(data, fh)
fh.close()

cur.close()
print(count, "records written to mmap.json")
