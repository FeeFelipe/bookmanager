import logging
from django.db import transaction

from book.infrastructure.repository.book_model import BookModel
from branch.infrastructure.branch_model import BranchModel
from book_stock.domain.book_stock_command_interface import BookStockCommandInterface
from book_stock.domain.book_stock_query_interface import BookStockQueryInterface
from book_stock.domain.book_stock_entities import BookStock
from .book_stock_model import BookStockModel


class BookStockRepository(BookStockCommandInterface, BookStockQueryInterface):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_all(self) -> list[BookStock]:
        self.logger.info("[BookStockRepository] Fetching all book stock records from the database")
        stocks = BookStockModel.objects.all()
        return [self._to_entity(obj) for obj in stocks]

    def get_by_id(self, book_stock_id: int) -> BookStock:
        self.logger.info(f"[BookStockRepository] Fetching book stock with ID {book_stock_id}")
        try:
            obj = BookStockModel.objects.get(id=book_stock_id)
            self.logger.info(f"[BookStockRepository] Book stock {book_stock_id} retrieved successfully")
            return self._to_entity(obj)
        except BookStockModel.DoesNotExist:
            self.logger.warning(f"[BookStockRepository] Book stock {book_stock_id} not found in the database")
            raise
        except Exception:
            self.logger.exception(f"[BookStockRepository] Unexpected error fetching book stock {book_stock_id}")
            raise

    def create(self, book_stock: BookStock) -> BookStock:
        self.logger.info(f"[BookStockRepository] Creating book stock entry: {book_stock}")
        try:
            data = book_stock.__dict__.copy()
            data.pop("id", None)
            data["book"] = BookModel.objects.get(id=book_stock.book)
            data["branch"] = BranchModel.objects.get(id=book_stock.branch)

            obj = BookStockModel.objects.create(**data)
            self.logger.info(f"[BookStockRepository] Book stock created with ID {obj.id}")
            return self._to_entity(obj)
        except Exception:
            self.logger.exception("[BookStockRepository] Unexpected error creating book stock")
            raise

    def update(self, book_stock_id: int, book_stock: BookStock) -> BookStock:
        self.logger.info(f"[BookStockRepository] Updating book stock {book_stock_id} with data: {book_stock}")
        try:
            data = book_stock.__dict__.copy()
            data.pop("id", None)
            data["book"] = BookModel.objects.get(id=book_stock.book)
            data["branch"] = BranchModel.objects.get(id=book_stock.branch)

            updated = BookStockModel.objects.filter(id=book_stock_id).update(**data)
            if updated == 0:
                self.logger.warning(f"[BookStockRepository] Book stock {book_stock_id} not found for update")
                raise BookStockModel.DoesNotExist(f"BookStock {book_stock_id} not found")

            obj = BookStockModel.objects.get(id=book_stock_id)
            self.logger.info(f"[BookStockRepository] Book stock {book_stock_id} updated successfully")
            return self._to_entity(obj)
        except Exception:
            self.logger.exception(f"[BookStockRepository] Unexpected error updating book stock {book_stock_id}")
            raise

    def delete(self, book_stock_id: int) -> None:
        self.logger.info(f"[BookStockRepository] Deleting book stock ID {book_stock_id}")
        try:
            deleted, _ = BookStockModel.objects.filter(id=book_stock_id).delete()
            if deleted == 0:
                self.logger.warning(f"[BookStockRepository] Book stock {book_stock_id} not found for deletion")
                raise BookStockModel.DoesNotExist(f"BookStock {book_stock_id} not found")
            self.logger.info(f"[BookStockRepository] Book stock {book_stock_id} deleted successfully")
        except Exception:
            self.logger.exception(f"[BookStockRepository] Unexpected error deleting book stock {book_stock_id}")
            raise

    def move_copy(self, book_stock_id: int, new_status: str) -> BookStock:
        self.logger.info(f"[BookStockRepository] Moving copy {book_stock_id} to status '{new_status}'")
        try:
            with transaction.atomic():
                copy = BookStockModel.objects.select_for_update().get(id=book_stock_id)

                if copy.status != 'available':
                    self.logger.warning(
                        f"[BookStockRepository] Copy {book_stock_id} with status '{copy.status}' cannot be moved"
                    )
                    raise ValueError("Copy is not available")

                copy.status = new_status
                copy.save()

                self.logger.info(f"[BookStockRepository] Copy {book_stock_id} successfully updated to '{new_status}'")
                return self._to_entity(copy)
        except BookStockModel.DoesNotExist:
            self.logger.warning(f"[BookStockRepository] Copy {book_stock_id} not found")
            raise
        except Exception:
            self.logger.exception(f"[BookStockRepository] Failed to move copy {book_stock_id}")
            raise

    def _to_entity(self, obj: BookStockModel) -> BookStock:
        return BookStock(
            id=obj.id,
            book=obj.book,
            branch=obj.branch,
            shelf=obj.shelf,
            floor=obj.floor,
            room=obj.room,
            status=obj.status,
        )
