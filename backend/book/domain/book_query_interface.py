from abc import ABC, abstractmethod

from .book_entities import Book


class BookQueryInterface(ABC):
    @abstractmethod
    def get_all(self) -> list[Book]:
        pass

    @abstractmethod
    def get_by_id(self, book_id: int) -> Book:
        pass
