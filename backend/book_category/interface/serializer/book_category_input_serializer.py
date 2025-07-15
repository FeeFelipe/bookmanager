from rest_framework import serializers


class BookCategoryInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
