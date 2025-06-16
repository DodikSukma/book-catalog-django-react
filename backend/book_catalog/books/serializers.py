from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
        extra_kwargs = {
            'title': {'required': True, 'max_length': 200},
            'author': {'required': True, 'max_length': 100},
            'cover': {'required': False, 'allow_blank': True},
            'description': {'required': False, 'allow_blank': True},
        }

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_author(self, value):
        if not value:
            raise serializers.ValidationError("Author cannot be empty.")
        return value

    def validate_cover(self, value):
        if value and not value.startswith(('http://', 'https://')):
            raise serializers.ValidationError("Cover URL must start with 'http://' or 'https://'.")
        return value

    def validate_description(self, value):
        if not value:
            raise serializers.ValidationError("Description cannot be empty.")
        return value
