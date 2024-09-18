from rest_framework import serializers
from .models import Book, BookUserLog, BorrowBookLog


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publishers', 'category', 'isBorrowed']
        read_only_fields = ['id']


class BookUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookUserLog
        fields = "__all__"
        read_only_fields = ['id']


class BorrowBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowBookLog
        fields = "__all__"
        read_only_fields = ['id', 'book']


class CustomBorrowBookSerializer(serializers.Serializer):
    book_user = serializers.CharField()
    books = serializers.ListField(child=serializers.CharField())


class CustomUnavailableBorrowBookSerializer(serializers.Serializer):
    book_title = serializers.CharField()
    duration = serializers.IntegerField()
    days_remaining = serializers.IntegerField()
