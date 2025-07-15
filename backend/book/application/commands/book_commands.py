import logging
from datetime import date, datetime
from abc import ABC

from book.domain.book_command_interface import BookCommandInterface
from book.domain.book_entities import Book
from book.infrastructure.repository.book_repository import BookRepository
from book.infrastructure.repository.book_search_repository import BookSearchRepository
from book.application.task.create_book_task import create_book_task


class BookCommands(BookCommandInterface, ABC):
    def __init__(self):
        self.repository = BookRepository()
        self.logger = logging.getLogger(__name__)

    def create(self, book: Book) -> Book:
        self.logger.info(f"[BookCommands] Queuing book for creation: {book.title}")
        data = {
            k: (v.isoformat() if isinstance(v, (date, datetime)) else v)
            for k, v in book.__dict__.items()
        }
        create_book_task.send(data)
        return Book(**data)

    def update(self, book_id: int, book: Book) -> Book:
        self.logger.info(f"[BookCommands] Updating book with ID: {book_id}")
        existing = self.repository.get_by_id(book_id)

        if not existing:
            self.logger.warning(f"[BookCommands] Attempt to update non-existent book ID: {book_id}")
            raise ValueError("Book not found")

        book.id = book_id
        updated = self.repository.update(book_id, book)
        self.logger.info(f"[BookCommands] Book ID {book_id} updated successfully")

        BookSearchRepository().index_book({
            "isbn": updated.isbn,
            "title": updated.title,
            "synopsis": updated.synopsis,
            "authors": [a.name for a in updated.authors],
            "categories": [c.name for c in updated.categories],
            "publication_date": updated.publication_date.isoformat(),
        })

        return updated

    def delete(self, book_id: int) -> None:
        self.logger.info(f"[BookCommands] Deleting book with ID: {book_id}")
        book = self.repository.get_by_id(book_id)
        if not book:
            self.logger.warning(f"[BookCommands] Attempt to delete non-existent book ID: {book_id}")
            raise ValueError("Book not found")

        self.repository.delete(book_id)
        BookSearchRepository.delete_book(book.isbn)
        self.logger.info(f"[BookCommands] Book ID {book_id} deleted successfully")
