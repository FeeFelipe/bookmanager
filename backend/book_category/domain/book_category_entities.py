from dataclasses import dataclass
from typing import Optional


@dataclass
class BookCategory:
    name: str
    id: Optional[int] = None
