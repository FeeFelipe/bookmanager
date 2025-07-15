from dataclasses import dataclass
from typing import Optional

from book.domain.book_entities import Book
from branch.domain.branch_entities import Branch


@dataclass
class BookStock:
    book: Book
    branch: Branch
    shelf: str
    floor: str
    room: str
    status: str
    id: Optional[int] = None
