import logging

from django.db import IntegrityError

from book.domain.book_command_interface import BookCommandInterface
from book.domain.book_entities import Book
from book.domain.book_query_interface import BookQueryInterface
from .book_model import BookModel


class BookRepository(BookCommandInterface, BookQueryInterface):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_all(self) -> list[Book]:
        self.logger.info("[BookRepository] get_all() called")
        books = BookModel.objects.all()
        return [self._to_entity(obj) for obj in books]

    def get_queryset(self):
        self.logger.info("[BookRepository] get_queryset() called")
        return BookModel.objects.all()

    def get_by_id(self, book_id: int) -> Book:
        self.logger.info(f"[BookRepository] get_by_id({book_id}) called")
        try:
            obj = BookModel.objects.get(id=book_id)
            self.logger.info(f"[BookRepository] Book {book_id} fetched successfully")
            return self._to_entity(obj)
        except BookModel.DoesNotExist:
            self.logger.warning(f"[BookRepository] Book {book_id} not found in database")
            raise
        except Exception:
            self.logger.exception(f"[BookRepository] Unexpected error fetching book {book_id}")
            raise

    def create(self, book: Book) -> Book:
        self.logger.info(f"[BookRepository] create() called with ISBN: {book.isbn}")
        try:
            data = book.__dict__.copy()
            data.pop("id", None)
            authors = data.pop("authors", [])
            categories = data.pop("categories", [])

            obj = BookModel.objects.create(**data)
            obj.authors.set(authors)
            obj.categories.set(categories)

            self.logger.info(f"[BookRepository] Book created with ID {obj.id}")
            return self._to_entity(obj)

        except IntegrityError:
            self.logger.warning(f"[BookRepository] Duplicate key error on ISBN: {book.isbn}")
            raise
        except Exception:
            self.logger.exception("[BookRepository] Unexpected error creating book")
            raise

    def update(self, book_id: int, book: Book) -> Book:
        self.logger.info(f"[BookRepository] update({book_id}) called with ISBN: {book.isbn}")
        try:
            data = book.__dict__.copy()
            data.pop("id", None)
            authors = data.pop("authors", [])
            categories = data.pop("categories", [])

            updated = BookModel.objects.filter(id=book_id).update(**data)
            if updated == 0:
                self.logger.warning(f"[BookRepository] Book {book_id} not found for update")
                raise BookModel.DoesNotExist(f"Book {book_id} not found")

            obj = BookModel.objects.get(id=book_id)
            obj.authors.set(authors)
            obj.categories.set(categories)

            self.logger.info(f"[BookRepository] Book {book_id} updated successfully")
            return self._to_entity(obj)

        except Exception:
            self.logger.exception(f"[BookRepository] Unexpected error updating book {book_id}")
            raise

    def delete(self, book_id: int) -> None:
        self.logger.info(f"[BookRepository] delete({book_id}) called")
        try:
            deleted, _ = BookModel.objects.filter(id=book_id).delete()
            if deleted == 0:
                self.logger.warning(f"[BookRepository] Book {book_id} not found for deletion")
                raise BookModel.DoesNotExist(f"Book {book_id} not found")

            self.logger.info(f"[BookRepository] Book {book_id} deleted successfully")
        except Exception:
            self.logger.exception(f"[BookRepository] Unexpected error deleting book {book_id}")
            raise

    def _to_entity(self, obj: BookModel) -> Book:
        return Book(
            id=obj.id,
            title=obj.title,
            isbn=obj.isbn,
            publisher=obj.publisher,
            edition=obj.edition,
            language=obj.language,
            book_type=obj.book_type,
            synopsis=obj.synopsis,
            publication_date=obj.publication_date,
            authors=list(obj.authors.all()),
            categories=list(obj.categories.all()),
        )
