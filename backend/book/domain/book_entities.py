from dataclasses import dataclass
from datetime import date
from typing import Optional

from author.domain.author_entities import Author
from book_category.domain.book_category_entities import BookCategory


@dataclass
class Book:
    title: str
    isbn: str
    publisher: str
    edition: str
    language: str
    book_type: str
    synopsis: Optional[str]
    publication_date: date
    authors: list[Author]
    categories: list[BookCategory]
    id: Optional[int] = None
