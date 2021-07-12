#print information about data
import sqlite3

conn = sqlite3.connect('nmeteorite.sqlite')
cur = conn.cursor()

cur.execute('SELECT id, recclass FROM Class')
recclass = dict()
for row in cur:
    recclass[row[0]] = row[1]

cur.execute('SELECT id, fall FROM FallStatus')
fallstatus = dict()
for row in cur:
    fallstatus[row[0]] = row[1]

cur.execute('SELECT id, nametype FROM Nametype')
nametype = dict()
for row in cur:
    nametype[row[0]] = row[1]

cur.execute('SELECT id, name, type_id, year FROM Landings')
landings = dict()
for row in cur:
    landings[row[0]] = (row[1], row[2], row[3])

print("Loaded landings=",len(landings)," classes=",len(recclass),
      " fall status=",len(fallstatus)," nametype=",len(nametype))
