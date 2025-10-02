# Meteorite JSON Pipeline

A clean, class-based Python pipeline that downloads NASA meteorite landing data, reverse-geocodes coordinates via Google Geocoding, normalizes into a small star schema in SQLite, and exports a map-ready JSON file.

**Why this repo?** It's a professional rework of a set of script files into a maintainable package with a simple CLI and clear steps: `load-raw → geocode → normalize → export`.

## Features
- **Class-based steps**: `LoadRawETL`, `GeocodeETL`, `NormalizeETL`, `ExportJson`.
- **SQLite storage** with reproducible schemas (`raw_meteorite.sqlite`, `location_data.sqlite`, `dw_meteorite.sqlite`).
- **Google Geocoding** integration (reverse geocode to country) – driven by env var `GOOGLE_API_KEY`.
- **Single command** orchestration: `python -m meteorite_pipeline run all` (or run steps individually).
- **No secrets in code**: all keys via environment variables or `.env` (optional).

## Quickstart

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt

# (optional) create a .env with GOOGLE_API_KEY=...

# Run everything (may take a while due to API calls)
python -m meteorite_pipeline run all

# Or step-by-step:
python -m meteorite_pipeline run load-raw
python -m meteorite_pipeline run geocode
python -m meteorite_pipeline run normalize
python -m meteorite_pipeline run export
```

## Configuration
The defaults are sane, but you can override via env vars:

- `GOOGLE_API_KEY` (required for geocoding step)
- `NASA_ENDPOINT` (default: https://data.nasa.gov/api/views/gh4g-9sfh/rows.json)
- `RAW_DB_PATH` (default: raw_meteorite.sqlite)
- `LOC_DB_PATH` (default: location_data.sqlite)
- `DW_DB_PATH` (default: dw_meteorite.sqlite)
- `OUTPUT_JSON` (default: mmap.json)

You can also pass overrides on the CLI: `--raw-db`, `--loc-db`, `--dw-db`, `--output`.

## Repo Layout

```
meteorite-json-pipeline/
├─ meteorite_pipeline/
│  ├─ __init__.py
│  ├─ cli.py                # argparse CLI entry point
│  ├─ config.py             # Settings dataclass + env loading
│  ├─ models.py             # Typed containers / helpers
│  ├─ clients/
│  │  ├─ nasa.py            # NASA client
│  │  └─ geocode.py         # Google reverse geocoder
│  ├─ storage/
│  │  ├─ schemas.py         # DDL for raw/dw/location SQLite
│  │  └─ sqlite.py          # SQLite helpers
│  ├─ steps/
│  │  ├─ load_raw.py        # LoadRawETL
│  │  ├─ geocode.py         # GeocodeETL
│  │  ├─ normalize.py       # NormalizeETL
│  │  └─ export_json.py     # ExportJson
│  └─ utils/
│     └─ http.py            # requests session, retry
├─ tests/                   # test scaffold
├─ docs/
│  └─ architecture.md
├─ .github/workflows/
│  └─ lint.yml              # flake8 / basic CI
├─ .gitignore
├─ requirements.txt
└─ LICENSE
```

## Output
Creates a `mmap.json` with:

```json
{
  "landings": [
    {
      "name": "abarla",
      "mass_grams": 1000.0,
      "reclat": 44.35,
      "reclong": -112.55,
      "year": 1965,
      "fall": "fell",
      "recclass": "H5",
      "country": "United States"
    }
  ]
}
```

## Notes
- Be respectful of Google API quotas. The geocoding step caches results in `location_data.sqlite` and won't refetch known lat/lng pairs.
- If you want to avoid Google entirely, you can skip `geocode` and proceed (country will be nulls).

---

MIT © 2025