import json
from ..config import Settings
from ..storage.sqlite import connect

class ExportJson:
    def __init__(self, s: Settings):
        self.s = s

    def run(self):
        data = {"landings": []}
        with connect(self.s.dw_db, readonly=True) as dw:
            cur = dw.cursor()
            cur.execute('''
                SELECT L.name, L.mass_grams, L.reclat, L.reclong, L.year,
                       F.fall, C.recclass, CO.country
                FROM Landings L
                LEFT JOIN Class C ON L.class_id = C.id
                LEFT JOIN FallStatus F ON L.fall_id = F.id
                LEFT JOIN Country CO ON L.country_id = CO.id
            ''')
            for row in cur.fetchall():
                name = (row[0] or "").replace("'", "")
                data["landings"].append({
                    "name": name,
                    "mass_grams": row[1],
                    "reclat": row[2],
                    "reclong": row[3],
                    "year": row[4],
                    "fall": row[5],
                    "recclass": row[6],
                    "country": row[7]
                })
        with open(self.s.output_json, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        print(f"Wrote {len(data['landings'])} records to {self.s.output_json}")