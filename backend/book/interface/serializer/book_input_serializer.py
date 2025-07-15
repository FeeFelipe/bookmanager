from rest_framework import serializers


class BookInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    isbn = serializers.CharField(max_length=20)
    publisher = serializers.CharField(max_length=255)
    edition = serializers.CharField(max_length=50)
    language = serializers.CharField(max_length=50)
    book_type = serializers.CharField(max_length=50)
    synopsis = serializers.CharField()
    publication_date = serializers.DateField()
    authors = serializers.ListField(child=serializers.IntegerField())
    categories = serializers.ListField(child=serializers.IntegerField())
