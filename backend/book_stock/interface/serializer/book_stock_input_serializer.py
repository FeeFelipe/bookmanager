from rest_framework import serializers


class BookStockInputSerializer(serializers.Serializer):
    book = serializers.IntegerField()
    branch = serializers.IntegerField()
    shelf = serializers.CharField(max_length=255)
    floor = serializers.CharField(max_length=255)
    room = serializers.CharField(max_length=255)
    status = serializers.CharField(max_length=50)
