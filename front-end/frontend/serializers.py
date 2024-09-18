from rest_framework import serializers
from .models import BookLog, BookUser, BorrowBook


class BookLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookLog
        fields = ["id", 'book_id', 'title', 'publishers', 'category', 'isBorrowed']
        read_only_fields = ['id']


class BookUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookUser
        fields = "__all__"
        read_only_fields = ['id']


class BorrowBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowBook
        fields = "__all__"
        read_only_fields = ['id', 'book']
