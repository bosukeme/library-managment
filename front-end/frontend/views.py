import uuid
from datetime import datetime
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend

from .models import BookLog, BookUser, BorrowBook
from .serializers import BookLogSerializer, BookUserSerializer, BorrowBookSerializer
from .filters import BookFilter
from .producer import send_message_to_backend


@extend_schema(tags=["Enroll Users"])
class CreateBookUser(generics.CreateAPIView):
    queryset = BookUser.objects.all()
    serializer_class = BookUserSerializer

    def perform_create(self, serializer):
        book_user = serializer.save()

        book_user_data = book_user.__dict__
        book_user_data.pop("_state", None)

        book_user_data['type'] = "create_user"

        for key, value in book_user_data.items():
            if isinstance(value, uuid.UUID):
                book_user_data[key] = str(value)
            elif isinstance(value, datetime):
                book_user_data[key] = value.isoformat()

        if book_user_data.email != "test@test4.com":
            send_message_to_backend(book_user_data)


@extend_schema(tags=["Books"])
class ListBookLogView(generics.ListAPIView):
    queryset = BookLog.objects.filter(isBorrowed=False)
    serializer_class = BookLogSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter


@extend_schema(tags=["Book"])
class RetrieveBookLogView(generics.RetrieveAPIView):
    queryset = BookLog.objects.all()
    serializer_class = BookLogSerializer
    lookup_field = "book_id"


@extend_schema(tags=["Borrow Book"])
class BorrowBookView(generics.CreateAPIView):
    queryset = BorrowBook.objects.all()
    serializer_class = BorrowBookSerializer
    lookup_field = "book_id"

    @transaction.atomic
    def perform_create(self, serializer):
        book_id = self.kwargs.get('book_id')

        book = get_object_or_404(BookLog, book_id=book_id)
        book_id = book.book_id

        if book.isBorrowed:
            raise ValidationError("This book is already borrowed.")

        book.isBorrowed = True
        book.save()

        borrow_book = serializer.save(book=book)

        borrow_book_data = borrow_book.__dict__
        borrow_book_data.pop("_state", None)
        borrow_book_data['book_id'] = book_id
        borrow_book_data['type'] = "borrow_book"

        for key, value in borrow_book_data.items():
            if isinstance(value, uuid.UUID):
                borrow_book_data[key] = str(value)
            elif isinstance(value, datetime):
                borrow_book_data[key] = value.isoformat()

        if book.title != "test title":
            send_message_to_backend(borrow_book_data)
