from abc import ABC, abstractmethod

from .book_entities import Book


class BookCommandInterface(ABC):
    @abstractmethod
    def create(self, book: Book) -> Book:
        pass

    @abstractmethod
    def update(self, book_id: int, book: Book) -> Book:
        pass

    @abstractmethod
    def delete(self, book_id: int) -> None:
        pass
