from typing import Iterable
from ..utils.http import make_session

class NasaClient:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.session = make_session()

    def fetch_rows(self) -> dict:
        r = self.session.get(self.endpoint, timeout=30)
        r.raise_for_status()
        return r.json()