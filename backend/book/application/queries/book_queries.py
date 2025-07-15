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
        self.logger.info("[BookQueries] get_all() called")
        books = self.repository.get_all()
        self.logger.info(f"[BookQueries] get_all() returned {len(books)} records")
        return books

    def get_by_id(self, book_id: int) -> Book | None:
        self.logger.info(f"[BookQueries] get_by_id({book_id}) called")
        try:
            book = self.repository.get_by_id(book_id)
            self.logger.info(f"[BookQueries] Book {book_id} found: title='{book.title}'")
            return book
        except BookModel.DoesNotExist:
            self.logger.warning(f"[BookQueries] Book {book_id} not found")
            return None
        except Exception:
            self.logger.exception(f"[BookQueries] Unexpected error retrieving book {book_id}")
            return None

    def get_queryset(self):
        self.logger.info("[BookQueries] get_queryset() called")
        return self.repository.get_queryset()
