from abc import ABC, abstractmethod

from .book_category_entities import BookCategory


class BookCategoryCommandInterface(ABC):
    @abstractmethod
    def create(self, book_category: BookCategory) -> BookCategory:
        pass

    @abstractmethod
    def update(self, book_category_id: int, book_category: BookCategory) -> BookCategory:
        pass

    @abstractmethod
    def delete(self, book_category_id: int) -> None:
        pass
