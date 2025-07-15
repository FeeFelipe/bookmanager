from dataclasses import dataclass
from typing import Optional


@dataclass
class Branch:
    name: str
    location: str
    id: Optional[int] = None
