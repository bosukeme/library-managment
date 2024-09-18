import uuid
from datetime import datetime
from collections import defaultdict
from django.utils import timezone

from rest_framework import generics
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from .producer import send_message_to_frontend

from .serializers import BookSerializer, BookUserSerializer, CustomBorrowBookSerializer, CustomUnavailableBorrowBookSerializer

from .models import Book, BookUserLog, BorrowBookLog
from .filters import BookFilter


@extend_schema(tags=["Add New Book"])
class CreateListBookView(generics.ListCreateAPIView):
    queryset = Book.objects.filter(isBorrowed=False)
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter

    def perform_create(self, serializer):
        book = serializer.save()
        book_data = book.__dict__
        book_data.pop("_state", None)

        book_data['type'] = "create"

        for key, value in book_data.items():
            if isinstance(value, uuid.UUID):
                book_data[key] = str(value)
            elif isinstance(value, datetime):
                book_data[key] = value.isoformat()
        send_message_to_frontend(book_data)


@extend_schema(tags=["book"])
class RetrieveDeleteBooksView(generics.RetrieveDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_object(self):
        book_id = self.kwargs.get('book_id')
        return get_object_or_404(Book, id=book_id)

    def perform_destroy(self, instance):

        book_data = {
            'id': str(instance.id),
            'title': instance.title,
            'publishers': instance.publishers,
            'category': instance.category,
            'isBorrowed': instance.isBorrowed,
            'type': 'delete'
        }

        super().perform_destroy(instance)

        for key, value in book_data.items():
            if isinstance(value, uuid.UUID):
                book_data[key] = str(value)
            elif isinstance(value, datetime):
                book_data[key] = value.isoformat()

        send_message_to_frontend(book_data)


@extend_schema(tags=["List Book Users Enrolled"])
class ListBookUsers(generics.ListAPIView):
    queryset = BookUserLog.objects.all()
    serializer_class = BookUserSerializer


@extend_schema(tags=["User Books Borrowed"])
class ListUsersBorrowedBooks(generics.ListAPIView):
    serializer_class = CustomBorrowBookSerializer
    queryset = BorrowBookLog.objects.all()

    def get_queryset(self):

        all_borrowed_books_users = BorrowBookLog.objects.select_related('bookuser', 'book')

        users_with_books = defaultdict(list)

        for borrow in all_borrowed_books_users:
            users_with_books[borrow.bookuser.firstname].append(borrow.book.title)

        result = [
            {
                "book_user": user,
                "books": books
            }
            for user, books in users_with_books.items()
        ]

        return result


@extend_schema(tags=["Unavailable Borrowed Books"])
class BooksNotAvailable(generics.ListAPIView):
    serializer_class = CustomUnavailableBorrowBookSerializer
    queryset = BorrowBookLog.objects.all()

    def get_queryset(self):
        all_borrowed_books = BorrowBookLog.objects.values('book__title', 'duration', 'created_at')

        borrowed_books = []
        for item in all_borrowed_books:

            borrowed_duration = item['duration']
            days_elapsed = (timezone.now() - item['created_at']).days
            days_remaining = max(borrowed_duration - days_elapsed, 0)

            borrowed_books.append({
                    'book_title': item['book__title'],
                    'duration': item['duration'],
                    'days_remaining': days_remaining
                })

        return borrowed_books
