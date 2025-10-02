from ..config import Settings
from ..clients.nasa import NasaClient
from ..storage.sqlite import init_raw, connect

class LoadRawETL:
    def __init__(self, s: Settings):
        self.s = s
        init_raw(self.s.raw_db)

    def run(self):
        client = NasaClient(self.s.nasa_endpoint)
        data = client.fetch_rows()
        rows = data.get("data", [])

        with connect(self.s.raw_db) as conn:
            cur = conn.cursor()
            for item in rows:
                name = (item[8] or "").strip().lower()
                if not name:
                    continue
                nametype = (item[10] or "").strip().lower() if item[10] else None
                recclass = (item[11] or "").strip().lower() if item[11] else None
                mass_grams = item[12]
                fall = (item[13] or "").strip().lower() if item[13] else None
                year = None
                if item[14]:
                    year = str(item[14])[:4]
                    try:
                        year = int(year)
                    except:
                        year = None
                reclat = item[15]
                reclong = item[16]

                cur.execute(
                    '''INSERT OR IGNORE INTO Landings
                       (name, nametype, recclass, mass_grams, fall, year, reclat, reclong)
                       VALUES (?,?,?,?,?,?,?,?)''',
                    (name, nametype, recclass, mass_grams, fall, year, reclat, reclong)
                )