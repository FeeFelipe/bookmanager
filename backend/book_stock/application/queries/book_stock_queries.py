import logging

from book_stock.domain.book_stock_entities import BookStock
from book_stock.domain.book_stock_query_interface import BookStockQueryInterface
from book_stock.infrastructure.book_stock_model import BookStockModel
from book_stock.infrastructure.book_stock_repository import BookStockRepository


class BookStockQueries(BookStockQueryInterface):
    def __init__(self):
        self.repository = BookStockRepository()
        self.logger = logging.getLogger(__name__)

    def get_all(self) -> list[BookStock]:
        book_stocks = self.repository.get_all()
        self.logger.info(f"[BookStockQueries] Retrieved {len(book_stocks)} book_stock records")
        return book_stocks

    def get_by_id(self, book_stock_id: int) -> BookStock | None:
        try:
            book_stock = self.repository.get_by_id(book_stock_id)
            self.logger.info(f"[BookStockQueries] BookStock found with ID: {book_stock_id}")
            return book_stock
        except BookStockModel.DoesNotExist:
            self.logger.warning(f"[BookStockQueries] BookStock with ID {book_stock_id} not found")
            return None
