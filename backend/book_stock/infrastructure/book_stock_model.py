from django.db import models

from django.contrib.postgres.indexes import Index
from book.infrastructure.repository.book_model import BookModel
from branch.infrastructure.branch_model import BranchModel


class BookStockModel(models.Model):
    STATUS = (
        ('available', 'Disponível'),
        ('borrowed', 'Emprestado'),
        ('reserved', 'Reservado'),
        ('lost', 'Perdido'),
    )

    book = models.ForeignKey(BookModel, on_delete=models.CASCADE, related_name="book_stock_entries")
    branch = models.ForeignKey(BranchModel, on_delete=models.CASCADE, related_name="book_stock_entries")
    shelf = models.CharField(max_length=255)
    qshelf = models.CharField(max_length=255)
    floor = models.CharField(max_length=255)
    room = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS, default='available')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            Index(fields=["status"], name="bookstock_status_idx"),
        ]

    def __str__(self):
        return self.shelf
