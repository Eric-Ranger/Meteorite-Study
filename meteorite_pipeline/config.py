from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    nasa_endpoint: str = os.getenv("NASA_ENDPOINT", "https://data.nasa.gov/api/views/gh4g-9sfh/rows.json")
    google_api_key: str | None = os.getenv("GOOGLE_API_KEY")
    raw_db: str = os.getenv("RAW_DB_PATH", "raw_meteorite.sqlite")
    loc_db: str = os.getenv("LOC_DB_PATH", "location_data.sqlite")
    dw_db: str = os.getenv("DW_DB_PATH", "dw_meteorite.sqlite")
    output_json: str = os.getenv("OUTPUT_JSON", "mmap.json")