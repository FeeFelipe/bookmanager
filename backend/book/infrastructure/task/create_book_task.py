import logging
import dramatiq

from book.domain.book_entities import Book
from book.infrastructure.repository.book_search_repository import BookSearchRepository
from book.infrastructure.repository.book_repository import BookRepository

logger = logging.getLogger(__name__)

@dramatiq.actor(queue_name="books", max_retries=3, retry_when=lambda e: True)
def create_book_task(book_data: dict):
    logger.info(f"[BookWorker] Processing new book: {book_data}")

    try:
        book = Book(**book_data)
        repository = BookRepository()
        created = repository.create(book)

        if not created:
            logger.error("[BookWorker] Book creation failed, skipping Elasticsearch indexing.")
            return

        logger.info(f"[BookWorker] Book created with ID {created.id}")

        BookSearchRepository().index_book({
            "isbn": created.isbn,
            "title": created.title,
            "synopsis": created.synopsis,
            "authors": [a.name for a in created.authors],
            "categories": [c.name for c in created.categories],
            "publication_date": created.publication_date.isoformat(),
        })
        logger.info(f"[BookWorker] Book created with ID {created.id}")

    except Exception:
        logger.exception(f"[BookWorker] Failed to create book")
        raise
