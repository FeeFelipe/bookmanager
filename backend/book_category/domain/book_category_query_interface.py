from abc import ABC, abstractmethod

from .book_category_entities import BookCategory


class BookCategoryQueryInterface(ABC):
    @abstractmethod
    def get_all(self) -> list[BookCategory]:
        pass

    @abstractmethod
    def get_by_id(self, book_category_id: int) -> BookCategory:
        pass
