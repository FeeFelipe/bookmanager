import logging

from book_category.domain.book_category_entities import BookCategory
from book_category.domain.book_category_query_interface import BookCategoryQueryInterface
from book_category.infrastructure.book_category_model import BookCategoryModel
from book_category.infrastructure.book_category_repository import BookCategoryRepository


class BookCategoryQueries(BookCategoryQueryInterface):
    def __init__(self):
        self.repository = BookCategoryRepository()
        self.logger = logging.getLogger(__name__)

    def get_all(self) -> list[BookCategory]:
        categories = self.repository.get_all()
        self.logger.info(f"[BookCategoryQueries] Retrieved {len(categories)} book category records")
        return categories

    def get_by_id(self, book_category_id: int) -> BookCategory | None:
        try:
            category = self.repository.get_by_id(book_category_id)
            self.logger.info(f"[BookCategoryQueries] BookCategory found with ID: {book_category_id}")
            return category
        except BookCategoryModel.DoesNotExist:
            self.logger.warning(f"[BookCategoryQueries] BookCategory with ID {book_category_id} not found")
            return None
