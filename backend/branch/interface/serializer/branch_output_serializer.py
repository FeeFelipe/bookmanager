from rest_framework import serializers


class BranchOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255)
