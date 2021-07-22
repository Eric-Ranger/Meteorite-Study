#print information about data
import sqlite3

conn = sqlite3.connect('file:dw_meteorite.sqlite?mode=ro', uri=True)
cur = conn.cursor()

cur.execute('SELECT * FROM Landings')
dw_id = list()
dw_type = list()
dw_class = list()
dw_grams = list()
dw_fall = list()
dw_year = list()
dw_lat = list()
dw_lng = list()
dw_country = list()

for row in cur:

    if row[0] is not None:
        dw_id.append(row[0])

    if row[2] is not None:
        dw_type.append(row[2])

    if row[3] is not None:
        dw_class.append(row[3])

    if row[4] is not None:
        dw_grams.append(row[4])

    if row[5] is not None:
        dw_fall.append(row[5])

    if row[6] is not None:
        dw_year.append(row[6])

    if row[7] is not None:
        dw_lat.append(row[7])

    if row[8] is not None:
        dw_lng.append(row[8])

    if row[9] is not None:
        dw_country.append(row[9])

conn_1 = sqlite3.connect('file:raw_meteorite.sqlite?mode=ro', uri=True)
cur_1 = conn_1.cursor()

cur_1.execute('SELECT * FROM Landings')
raw_id = list()
raw_type = list()
raw_class = list()
raw_grams = list()
raw_fall = list()
raw_year = list()
raw_lat = list()
raw_lng = list()
raw_country = list()

for row in cur_1:

    if row[0] is not None:
        raw_id.append(row[0])

    if row[2] is not None:
        raw_type.append(row[2])

    if row[3] is not None:
        raw_class.append(row[3])

    if row[4] is not None:
        raw_grams.append(row[4])

    if row[5] is not None:
        raw_fall.append(row[5])

    if row[6] is not None:
        raw_year.append(row[6])

    if row[7] is not None:
        raw_lat.append(row[7])

    if row[8] is not None:
        raw_lng.append(row[8])

print("Row count for dw and raw data")
print("rows",len(dw_id),"type",len(dw_type),"class",len(dw_class),"grams",len(dw_grams),"fall",len(dw_fall),"year",len(dw_year),"lat",len(dw_lat),"lng",len(dw_lng),"country",len(dw_country))
print("rows",len(raw_id),"type",len(raw_type),"class",len(raw_class),"grams",len(raw_grams),"fall",len(raw_fall),"year",len(raw_year),"lat",len(raw_lat),"lng",len(raw_lng))
