import logging

from author.domain.author_entities import Author
from author.domain.author_query_interface import AuthorQueryInterface
from author.infrastructure.author_model import AuthorModel
from author.infrastructure.author_repository import AuthorRepository


class AuthorQueries(AuthorQueryInterface):
    def __init__(self):
        self.repository = AuthorRepository()
        self.logger = logging.getLogger(__name__)

    def get_all(self) -> list[Author]:
        authors = self.repository.get_all()
        self.logger.info(f"[AuthorQueries] Retrieved {len(authors)} author records")
        return authors

    def get_by_id(self, author_id: int) -> Author | None:
        try:
            author = self.repository.get_by_id(author_id)
            self.logger.info(f"[AuthorQueries] Author found with ID: {author_id}")
            return author
        except AuthorModel.DoesNotExist:
            self.logger.warning(f"[AuthorQueries] Author with ID {author_id} not found")
            return None
