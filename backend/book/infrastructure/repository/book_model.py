from django.db import models
from django.contrib.postgres.indexes import GinIndex, Index

from author.infrastructure.author_model import AuthorModel
from book_category.infrastructure.book_category_model import BookCategoryModel


class BookModel(models.Model):
    BOOK_TYPES = (
        ('physical', 'Físico'),
        ('ebook', 'eBook'),
    )

    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=20, unique=True)
    publisher = models.CharField(max_length=255)
    edition = models.CharField(max_length=50)
    language = models.CharField(max_length=100)
    book_type = models.CharField(max_length=10, choices=BOOK_TYPES)
    synopsis = models.TextField(blank=True, null=True)
    publication_date = models.DateField()

    authors = models.ManyToManyField(AuthorModel, related_name='books')
    categories = models.ManyToManyField(BookCategoryModel, related_name='books')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            GinIndex(fields=['title'], name='book_title_trgm_gin', opclasses=['gin_trgm_ops']),
            Index(fields=["isbn"], name="book_isbn_idx"),
        ]