from django.db import models

from utils.model_abstract import Model


class BookLog(Model):
    book_id = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    publishers = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    isBorrowed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class BookUser(Model):

    email = models.EmailField(unique=True)
    firstname = models.CharField(max_length=50, null=False)
    lastname = models.CharField(max_length=50, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.firstname} {self.lastname}"


class BorrowBook(Model):
    bookuser = models.ForeignKey(BookUser, on_delete=models.CASCADE, related_name="borrowed_books")
    book = models.ForeignKey(BookLog, on_delete=models.CASCADE, related_name="borrowed_books")
    duration = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.bookuser.firstname} borrowed {self.book.title} for {self.duration} days"
