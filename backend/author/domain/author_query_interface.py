from abc import ABC, abstractmethod

from .author_entities import Author


class AuthorQueryInterface(ABC):
    @abstractmethod
    def get_all(self) -> list[Author]:
        pass

    @abstractmethod
    def get_by_id(self, author_id: int) -> Author:
        pass
