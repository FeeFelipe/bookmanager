from dataclasses import dataclass
from typing import Optional


@dataclass
class Author:
    name: str
    id: Optional[int] = None
