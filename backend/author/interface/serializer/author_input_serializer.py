from rest_framework import serializers


class AuthorInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
