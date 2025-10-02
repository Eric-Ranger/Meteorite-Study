RAW_DDL = '''
CREATE TABLE IF NOT EXISTS Landings(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    nametype TEXT,
    recclass TEXT,
    mass_grams REAL,
    fall TEXT,
    year INTEGER,
    reclat REAL,
    reclong REAL
);
'''

LOC_DDL = '''
CREATE TABLE IF NOT EXISTS location(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lat REAL NOT NULL,
    lng REAL NOT NULL,
    json TEXT,
    CONSTRAINT unq_lat_lng UNIQUE (lat,lng) ON CONFLICT IGNORE
);
'''

DW_DDL = '''
CREATE TABLE IF NOT EXISTS Landings
 (id INTEGER PRIMARY KEY,
  name TEXT UNIQUE,
  type_id INTEGER,
  class_id INTEGER,
  mass_grams REAL,
  fall_id INTEGER,
  year INTEGER,
  reclat REAL,
  reclong REAL,
  country_id INTEGER);

CREATE TABLE IF NOT EXISTS Nametype
 (id INTEGER PRIMARY KEY, nametype TEXT UNIQUE);

CREATE TABLE IF NOT EXISTS Class
 (id INTEGER PRIMARY KEY, recclass TEXT UNIQUE);

CREATE TABLE IF NOT EXISTS FallStatus
 (id INTEGER PRIMARY KEY, fall TEXT UNIQUE);

CREATE TABLE IF NOT EXISTS Country
 (id INTEGER PRIMARY KEY, country TEXT UNIQUE);
'''