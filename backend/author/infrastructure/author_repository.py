import logging

from author.domain.author_command_interface import AuthorCommandInterface
from author.domain.author_entities import Author
from author.domain.author_query_interface import AuthorQueryInterface
from .author_model import AuthorModel


class AuthorRepository(AuthorCommandInterface, AuthorQueryInterface):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_all(self) -> list[Author]:
        self.logger.info("[AuthorRepository] Fetching all authors from database")
        authors = AuthorModel.objects.all()
        return [self._to_entity(obj) for obj in authors]

    def get_by_id(self, author_id: int) -> Author:
        try:
            obj = AuthorModel.objects.get(id=author_id)
            self.logger.info(f"[AuthorRepository] Author {author_id} fetched successfully")
            return self._to_entity(obj)
        except AuthorModel.DoesNotExist:
            self.logger.warning(f"[AuthorRepository] Author {author_id} not found in database")
            raise
        except Exception:
            self.logger.exception(f"[AuthorRepository] Unexpected error fetching author {author_id}")
            raise

    def create(self, author: Author) -> Author:
        try:
            data = author.__dict__.copy()
            data.pop("id", None)
            obj = AuthorModel.objects.create(**data)
            self.logger.info(f"[AuthorRepository] Author created with ID {obj.id}")
            return self._to_entity(obj)
        except Exception:
            self.logger.exception("[AuthorRepository] Unexpected error creating author")
            raise

    def update(self, author_id: int, author: Author) -> Author:
        try:
            data = author.__dict__.copy()
            data.pop("id", None)
            updated = AuthorModel.objects.filter(id=author_id).update(**data)
            if updated == 0:
                self.logger.warning(f"[AuthorRepository] Author {author_id} not found for update")
                raise AuthorModel.DoesNotExist(f"Author {author_id} not found")

            obj = AuthorModel.objects.get(id=author_id)
            self.logger.info(f"[AuthorRepository] Author {author_id} updated successfully")
            return self._to_entity(obj)
        except Exception:
            self.logger.exception(f"[AuthorRepository] Unexpected error updating author {author_id}")
            raise

    def delete(self, author_id: int) -> None:
        try:
            deleted, _ = AuthorModel.objects.filter(id=author_id).delete()
            if deleted == 0:
                self.logger.warning(f"[AuthorRepository] Author {author_id} not found for deletion")
                raise AuthorModel.DoesNotExist(f"Author {author_id} not found")
            self.logger.info(f"[AuthorRepository] Author {author_id} deleted successfully")
        except Exception:
            self.logger.exception(f"[AuthorRepository] Unexpected error deleting author {author_id}")
            raise

    def _to_entity(self, obj: AuthorModel) -> Author:
        return Author(
            id=obj.id,
            name=obj.name
        )
