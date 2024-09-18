from django.urls import path

from .views import BorrowBookView, ListBookLogView, RetrieveBookLogView, CreateBookUser


urlpatterns = [
    path("books/", ListBookLogView.as_view(), name="booklog-list"),
    path('books/<str:book_id>/', RetrieveBookLogView.as_view(), name='retrieve_book'),
    path("books/borrow/<str:book_id>/", BorrowBookView.as_view(), name="book-borrow"),
    path("users/", CreateBookUser.as_view(), name="bookuser-create"),
]
