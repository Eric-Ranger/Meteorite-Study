from dataclasses import dataclass
from typing import Optional

@dataclass
class Landing:
    name: str
    nametype: Optional[str]
    recclass: Optional[str]
    mass_grams: Optional[float]
    fall: Optional[str]
    year: Optional[int]
    reclat: Optional[float]
    reclong: Optional[float]