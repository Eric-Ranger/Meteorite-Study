from typing import Optional
from ..utils.http import make_session

class Geocoder:
    def __init__(self, api_key: str):
        self.session = make_session()
        self.api_key = api_key

    def reverse_country(self, lat: float, lng: float) -> Optional[dict]:
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {"latlng": f"{lat},{lng}", "key": self.api_key}
        r = self.session.get(url, params=params, timeout=20)
        r.raise_for_status()
        js = r.json()
        if js.get("status") == "ZERO_RESULTS":
            return None
        return js