import logging
from abc import ABC

from book_category.domain.book_category_command_interface import BookCategoryCommandInterface
from book_category.domain.book_category_entities import BookCategory
from book_category.infrastructure.book_category_repository import BookCategoryRepository


class BookCategoryCommands(BookCategoryCommandInterface, ABC):
    def __init__(self):
        self.repository = BookCategoryRepository()
        self.logger = logging.getLogger(__name__)

    def create(self, book_category: BookCategory) -> BookCategory:
        self.logger.info(f"[BookCategoryCommands] Creating new book category: {book_category.name}")
        created = self.repository.create(book_category)
        self.logger.info(f"[BookCategoryCommands] BookCategory created successfully with ID: {created.id}")
        return created

    def update(self, book_category_id: int, book_category: BookCategory) -> BookCategory:
        self.logger.info(f"[BookCategoryCommands] Updating book category with ID: {book_category_id}")
        existing = self.repository.get_by_id(book_category_id)
        if not existing:
            self.logger.warning(
                f"[BookCategoryCommands] Attempt to update non-existent book category ID: {book_category_id}")
            raise ValueError("BookCategory not found")

        book_category.id = book_category_id
        updated = self.repository.update(book_category_id, book_category)
        self.logger.info(f"[BookCategoryCommands] BookCategory ID {book_category_id} updated successfully")
        return updated

    def delete(self, book_category_id: int) -> None:
        self.logger.info(f"[BookCategoryCommands] Deleting book category with ID: {book_category_id}")
        book_category = self.repository.get_by_id(book_category_id)
        if not book_category:
            self.logger.warning(
                f"[BookCategoryCommands] Attempt to delete non-existent book category ID: {book_category_id}")
            raise ValueError("BookCategory not found")

        self.repository.delete(book_category_id)
        self.logger.info(f"[BookCategoryCommands] BookCategory ID {book_category_id} deleted successfully")
