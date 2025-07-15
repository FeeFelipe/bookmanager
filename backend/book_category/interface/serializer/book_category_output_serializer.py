from rest_framework import serializers


class BookCategoryOutputSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_id(self, obj):
        return getattr(obj, 'id', obj if isinstance(obj, int) else None)

    def get_name(self, obj):
        return getattr(obj, 'name', None)
