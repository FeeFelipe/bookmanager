from abc import ABC, abstractmethod

from .book_stock_entities import BookStock


class BookStockQueryInterface(ABC):
    @abstractmethod
    def get_all(self) -> list[BookStock]:
        pass

    @abstractmethod
    def get_by_id(self, book_stock_id: int) -> BookStock:
        pass
