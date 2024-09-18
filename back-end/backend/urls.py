from django.urls import path

from .views import CreateListBookView, RetrieveDeleteBooksView, ListBookUsers, ListUsersBorrowedBooks, BooksNotAvailable

urlpatterns = [
    path("users/", ListBookUsers.as_view(), name="bookuser-list"),
    path('borrowed-books/', ListUsersBorrowedBooks.as_view(), name='list-borrowed-books'),
    path('unavailable-borrowed-books/', BooksNotAvailable.as_view(), name='unavailable-borrowed-books'),
    path('books/', CreateListBookView.as_view(), name='create'),
    path('books/<str:book_id>/', RetrieveDeleteBooksView.as_view(), name='retrieve-delete'),
]
