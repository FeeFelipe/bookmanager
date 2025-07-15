from abc import ABC, abstractmethod

from .author_entities import Author


class AuthorCommandInterface(ABC):
    @abstractmethod
    def create(self, author: Author) -> Author:
        pass

    @abstractmethod
    def update(self, author_id: int, author: Author) -> Author:
        pass

    @abstractmethod
    def delete(self, author_id: int) -> None:
        pass
