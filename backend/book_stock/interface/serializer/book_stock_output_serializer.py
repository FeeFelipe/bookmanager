from rest_framework import serializers

from book.interface.serializer.book_output_serializer import BookOutputSerializer
from branch.interface.serializer.branch_output_serializer import BranchOutputSerializer


class BookStockOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    book = BookOutputSerializer()
    branch = BranchOutputSerializer()
    shelf = serializers.CharField(max_length=255)
    floor = serializers.CharField(max_length=255)
    room = serializers.CharField(max_length=255)
    status = serializers.CharField(max_length=50)
