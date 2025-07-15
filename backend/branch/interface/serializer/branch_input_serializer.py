from rest_framework import serializers


class BranchInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255)
