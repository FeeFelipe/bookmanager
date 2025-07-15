from rest_framework import serializers

from author.interface.serializer.author_output_serializer import AuthorOutputSerializer
from book_category.interface.serializer.book_category_output_serializer import BookCategoryOutputSerializer


class BookOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    isbn = serializers.CharField()
    publisher = serializers.CharField()
    edition = serializers.CharField()
    language = serializers.CharField()
    book_type = serializers.CharField()
    synopsis = serializers.CharField()
    publication_date = serializers.DateField()
    authors = AuthorOutputSerializer(many=True)
    categories = BookCategoryOutputSerializer(many=True)
