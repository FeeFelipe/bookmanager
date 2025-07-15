import logging
from abc import ABC

from author.domain.author_command_interface import AuthorCommandInterface
from author.domain.author_entities import Author
from author.infrastructure.author_repository import AuthorRepository


class AuthorCommands(AuthorCommandInterface, ABC):
    def __init__(self):
        self.repository = AuthorRepository()
        self.logger = logging.getLogger(__name__)

    def create(self, author: Author) -> Author:
        self.logger.info(f"[AuthorCommands] Creating new author: {author.name}")
        result = self.repository.create(author)
        self.logger.info(f"[AuthorCommands] Author created successfully with ID: {result.id}")
        return result

    def update(self, author_id: int, author: Author) -> Author:
        self.logger.info(f"[AuthorCommands] Updating author with ID: {author_id}")
        existing = self.repository.get_by_id(author_id)
        if not existing:
            self.logger.warning(f"[AuthorCommands] Attempt to update non-existent author ID: {author_id}")
            raise ValueError("Author not found")

        author.id = author_id
        updated = self.repository.update(author_id, author)
        self.logger.info(f"[AuthorCommands] Author ID {author_id} updated successfully")
        return updated

    def delete(self, author_id: int) -> None:
        self.logger.info(f"[AuthorCommands] Deleting author with ID: {author_id}")
        author = self.repository.get_by_id(author_id)
        if not author:
            self.logger.warning(f"[AuthorCommands] Attempt to delete non-existent author ID: {author_id}")
            raise ValueError("Author not found")

        self.repository.delete(author_id)
        self.logger.info(f"[AuthorCommands] Author ID {author_id} deleted successfully")
