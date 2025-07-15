import logging

from book.domain.book_entities import Book
from book.domain.book_query_interface import BookQueryInterface
from book.infrastructure.repository.book_model import BookModel
from book.infrastructure.repository.book_repository import BookRepository


class BookQueries(BookQueryInterface):
    def __init__(self):
        self.repository = BookRepository()
        self.logger = logging.getLogger(__name__)

    def get_all(self) -> list[Book]:
        books = self.repository.get_all()
        self.logger.info(f"[BookQueries] Retrieved {len(books)} book records")
        return books

    def get_by_id(self, book_id: int) -> Book | None:
        try:
            book = self.repository.get_by_id(book_id)
            self.logger.info(f"[BookQueries] Book found with ID: {book_id}")
            return book
        except BookModel.DoesNotExist:
            self.logger.warning(f"[BookQueries] Book with ID {book_id} not found")
            return None

    def get_queryset(self):
        return self.repository.get_queryset()
