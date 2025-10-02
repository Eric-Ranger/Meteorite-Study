# Architecture

**Goal:** Professionalize a set of scripts (NASA load, geocode, normalize, map JSON) into a clean, testable pipeline.

## Steps
1. **LoadRawETL** (`steps/load_raw.py`): Fetch NASA JSON rows and insert into `raw_meteorite.sqlite`.
2. **GeocodeETL** (`steps/geocode.py`): Reverse geocode `(reclat, reclong)` with Google; cache response in `location_data.sqlite`.
3. **NormalizeETL** (`steps/normalize.py`): Create a simple star schema in `dw_meteorite.sqlite`: `Landings`, `Nametype`, `Class`, `FallStatus`, `Country`.
4. **ExportJson** (`steps/export_json.py`): Join DW tables and write `mmap.json` for mapping/viz.

## Design
- Each step is an idempotent class with a `.run()` method.
- HTTP calls go through a retry-enabled session.
- Secrets via env vars (`GOOGLE_API_KEY`), no hard-coded keys.