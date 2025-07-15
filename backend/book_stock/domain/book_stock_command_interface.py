from abc import ABC, abstractmethod

from .book_stock_entities import BookStock


class BookStockCommandInterface(ABC):
    @abstractmethod
    def create(self, book_stock: BookStock) -> BookStock:
        pass

    @abstractmethod
    def update(self, book_stock_id: int, book_stock: BookStock) -> BookStock:
        pass

    @abstractmethod
    def delete(self, book_stock_id: int) -> None:
        pass
