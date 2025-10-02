from ..config import Settings
from ..clients.geocode import Geocoder
from ..storage.sqlite import init_loc, connect

class GeocodeETL:
    def __init__(self, s: Settings):
        self.s = s
        init_loc(self.s.loc_db)

    def run(self):
        if not self.s.google_api_key:
            print("GOOGLE_API_KEY not set; skipping geocode step.")
            return

        gc = Geocoder(self.s.google_api_key)

        # read unique lat/lng from raw
        with connect(self.s.raw_db, readonly=True) as raw:
            rc = raw.cursor()
            rc.execute("SELECT DISTINCT reclat, reclong FROM Landings WHERE reclat IS NOT NULL AND reclong IS NOT NULL")
            pairs = [(r[0], r[1]) for r in rc.fetchall()]

        # cache into location db
        with connect(self.s.loc_db) as loc:
            lc = loc.cursor()
            for lat, lng in pairs:
                # skip out-of-range
                if lat < -90 or lat > 90 or lng < -180 or lng > 180:
                    continue
                # check cache
                lc.execute("SELECT 1 FROM location WHERE lat=? AND lng=? LIMIT 1", (lat, lng))
                if lc.fetchone():
                    continue
                js = gc.reverse_country(lat, lng)
                if js is None:
                    continue
                lc.execute("INSERT OR IGNORE INTO location (lat, lng, json) VALUES (?,?,?)",
                           (lat, lng, json.dumps(js)))