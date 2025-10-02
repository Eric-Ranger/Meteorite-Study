import json
from ..config import Settings
from ..storage.sqlite import init_dw, connect

class NormalizeETL:
    def __init__(self, s: Settings):
        self.s = s
        init_dw(self.s.dw_db)

    def _get_country_from_cache(self, lat, lng, loc_cur):
        loc_cur.execute("SELECT json FROM location WHERE lat=? AND lng=? LIMIT 1", (lat, lng))
        row = loc_cur.fetchone()
        if not row:
            return None
        js = json.loads(row[0])
        if js.get("status") == "ZERO_RESULTS":
            return None
        for comp in js.get("results", [{}])[0].get("address_components", []):
            if "country" in comp.get("types", []):
                return comp.get("long_name")
        return None

    def run(self):
        with connect(self.s.raw_db, readonly=True) as raw,              connect(self.s.loc_db, readonly=True) as loc,              connect(self.s.dw_db) as dw:

            rc = raw.cursor()
            lc = loc.cursor()
            dc = dw.cursor()

            rc.execute("SELECT name, nametype, recclass, mass_grams, fall, year, reclat, reclong FROM Landings")
            for (name, nametype, recclass, mass, fall, year, lat, lng) in rc.fetchall():
                # country via cache
                country = None
                if lat and lng and not (lat == 0 and lng == 0):
                    country = self._get_country_from_cache(lat, lng, lc)

                # dims
                dc.execute("INSERT OR IGNORE INTO Nametype (nametype) VALUES (?)", (nametype,))
                dc.execute("SELECT id FROM Nametype WHERE nametype=? LIMIT 1", (nametype,))
                type_id = (dc.fetchone() or [None])[0]

                dc.execute("INSERT OR IGNORE INTO Class (recclass) VALUES (?)", (recclass,))
                dc.execute("SELECT id FROM Class WHERE recclass=? LIMIT 1", (recclass,))
                class_id = (dc.fetchone() or [None])[0]

                dc.execute("INSERT OR IGNORE INTO FallStatus (fall) VALUES (?)", (fall,))
                dc.execute("SELECT id FROM FallStatus WHERE fall=? LIMIT 1", (fall,))
                fall_id = (dc.fetchone() or [None])[0]

                country_id = None
                if country:
                    dc.execute("INSERT OR IGNORE INTO Country (country) VALUES (?)", (country,))
                    dc.execute("SELECT id FROM Country WHERE country=? LIMIT 1", (country,))
                    country_id = (dc.fetchone() or [None])[0]

                # fact
                dc.execute(
                    '''INSERT OR IGNORE INTO Landings
                       (name, type_id, class_id, mass_grams, fall_id, year, reclat, reclong, country_id)
                       VALUES (?,?,?,?,?,?,?,?,?)''',
                    (name, type_id, class_id, mass, fall_id, year, lat, lng, country_id)
                )