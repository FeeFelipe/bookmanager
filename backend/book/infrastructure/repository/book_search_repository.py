import logging
from config.es_client import es_client


class BookSearchRepository:
    INDEX = "books"

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def index_book(self, book: dict):
        self.logger.info(f"[BookSearchRepository] Indexing book with ISBN {book.get('isbn')}")
        try:
            es_client.index(index=self.INDEX, id=book["isbn"], document=book)
            self.logger.info(f"[BookSearchRepository] Book {book['isbn']} indexed successfully")
        except Exception:
            self.logger.exception(f"[BookSearchRepository] Failed to index book {book.get('isbn')}")
            raise

    def search_books(self, query: str) -> list:
        self.logger.info(f"[BookSearchRepository] Searching books with query: '{query}'")
        try:
            response = es_client.search(
                index=self.INDEX,
                query={
                    "multi_match": {
                        "query": query,
                        "fields": ["title^3", "synopsis", "authors"]
                    }
                }
            )
            hits = [hit["_source"] for hit in response["hits"]["hits"]]
            self.logger.info(f"[BookSearchRepository] Found {len(hits)} results for query: '{query}'")
            return hits
        except Exception:
            self.logger.exception(f"[BookSearchRepository] Failed to search books with query: '{query}'")
            raise

    def delete_book(self, isbn: str):
        self.logger.info(f"[BookSearchRepository] Deleting book with ISBN {isbn}")
        try:
            es_client.delete(index=self.INDEX, id=isbn, ignore=[404])
            self.logger.info(f"[BookSearchRepository] Book {isbn} deleted from index")
        except Exception:
            self.logger.exception(f"[BookSearchRepository] Failed to delete book with ISBN {isbn}")
            raise
