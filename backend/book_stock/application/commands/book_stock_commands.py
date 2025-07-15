import logging
from abc import ABC

from book_stock.domain.book_stock_command_interface import BookStockCommandInterface
from book_stock.domain.book_stock_entities import BookStock
from book_stock.infrastructure.book_stock_repository import BookStockRepository


class BookStockCommands(BookStockCommandInterface, ABC):
    def __init__(self):
        self.repository = BookStockRepository()
        self.logger = logging.getLogger(__name__)

    def create(self, book_stock: BookStock) -> BookStock:
        self.logger.info(f"[BookStockCommands] Creating new book_stock: {book_stock.book} - {book_stock.branch}")
        created = self.repository.create(book_stock)
        self.logger.info(f"[BookStockCommands] BookStock created successfully with ID: {created.id}")
        return created

    def update(self, book_stock_id: int, book_stock: BookStock) -> BookStock:
        self.logger.info(f"[BookStockCommands] Updating book_stock with ID: {book_stock_id}")
        existing = self.repository.get_by_id(book_stock_id)
        if not existing:
            self.logger.warning(f"[BookStockCommands] Attempt to update non-existent book_stock ID: {book_stock_id}")
            raise ValueError("BookStock not found")

        book_stock.id = book_stock_id
        updated = self.repository.update(book_stock_id, book_stock)
        self.logger.info(f"[BookStockCommands] BookStock ID {book_stock_id} updated successfully")
        return updated

    def delete(self, book_stock_id: int) -> None:
        self.logger.info(f"[BookStockCommands] Deleting book_stock with ID: {book_stock_id}")
        book_stock = self.repository.get_by_id(book_stock_id)
        if not book_stock:
            self.logger.warning(f"[BookStockCommands] Attempt to delete non-existent book_stock ID: {book_stock_id}")
            raise ValueError("BookStock not found")

        self.repository.delete(book_stock_id)
        self.logger.info(f"[BookStockCommands] BookStock ID {book_stock_id} deleted successfully")
