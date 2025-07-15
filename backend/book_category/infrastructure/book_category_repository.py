import logging

from book_category.domain.book_category_command_interface import BookCategoryCommandInterface
from book_category.domain.book_category_entities import BookCategory
from book_category.domain.book_category_query_interface import BookCategoryQueryInterface
from .book_category_model import BookCategoryModel


class BookCategoryRepository(BookCategoryCommandInterface, BookCategoryQueryInterface):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_all(self) -> list[BookCategory]:
        self.logger.info("[BookCategoryRepository] Fetching all book categories from database")
        categories = BookCategoryModel.objects.all()
        return [self._to_entity(obj) for obj in categories]

    def get_by_id(self, book_category_id: int) -> BookCategory:
        self.logger.info(f"[BookCategoryRepository] Fetching book category with ID {book_category_id}")
        try:
            obj = BookCategoryModel.objects.get(id=book_category_id)
            self.logger.info(f"[BookCategoryRepository] Book category {book_category_id} fetched successfully")
            return self._to_entity(obj)
        except BookCategoryModel.DoesNotExist:
            self.logger.warning(f"[BookCategoryRepository] Book category {book_category_id} not found")
            raise
        except Exception:
            self.logger.exception(f"[BookCategoryRepository] Unexpected error fetching book category {book_category_id}")
            raise

    def create(self, book_category: BookCategory) -> BookCategory:
        self.logger.info(f"[BookCategoryRepository] Creating book category: {book_category}")
        try:
            data = book_category.__dict__.copy()
            data.pop("id", None)
            obj = BookCategoryModel.objects.create(**data)
            self.logger.info(f"[BookCategoryRepository] Book category created with ID {obj.id}")
            return self._to_entity(obj)
        except Exception:
            self.logger.exception("[BookCategoryRepository] Unexpected error creating book category")
            raise

    def update(self, book_category_id: int, book_category: BookCategory) -> BookCategory:
        self.logger.info(f"[BookCategoryRepository] Updating book category {book_category_id} with data: {book_category}")
        try:
            data = book_category.__dict__.copy()
            data.pop("id", None)
            updated = BookCategoryModel.objects.filter(id=book_category_id).update(**data)
            if updated == 0:
                self.logger.warning(f"[BookCategoryRepository] Book category {book_category_id} not found for update")
                raise BookCategoryModel.DoesNotExist(f"BookCategory {book_category_id} not found")

            obj = BookCategoryModel.objects.get(id=book_category_id)
            self.logger.info(f"[BookCategoryRepository] Book category {book_category_id} updated successfully")
            return self._to_entity(obj)
        except Exception:
            self.logger.exception(f"[BookCategoryRepository] Unexpected error updating book category {book_category_id}")
            raise

    def delete(self, book_category_id: int) -> None:
        self.logger.info(f"[BookCategoryRepository] Deleting book category {book_category_id}")
        try:
            deleted, _ = BookCategoryModel.objects.filter(id=book_category_id).delete()
            if deleted == 0:
                self.logger.warning(f"[BookCategoryRepository] Book category {book_category_id} not found for deletion")
                raise BookCategoryModel.DoesNotExist(f"BookCategory {book_category_id} not found")
            self.logger.info(f"[BookCategoryRepository] Book category {book_category_id} deleted successfully")
        except Exception:
            self.logger.exception(f"[BookCategoryRepository] Unexpected error deleting book category {book_category_id}")
            raise

    def _to_entity(self, obj: BookCategoryModel) -> BookCategory:
        return BookCategory(
            id=obj.id,
            name=obj.name,
        )
