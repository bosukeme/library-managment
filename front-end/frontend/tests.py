import json
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from .models import BookLog, BookUser


class EnrollUserTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.data = {
            "email": "test@test4.com",
            "firstname": "test firstname",
            "lastname": "test lastname",
        }

        self.create_user_url = "/api/frontend/users/"

    def test_create_user(self):
        response = self.client.post(self.create_user_url, json.dumps(self.data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_failed(self):
        data = self.data
        data.pop("email")
        response = self.client.post(self.create_user_url, json.dumps(self.data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ListBooksTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_books_url = "/api/frontend/books/"

    def test_list_books(self):
        response = self.client.get(self.list_books_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RetrieveBookTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def create_book(self):
        bk = BookLog(
            book_id="8d41c47cb8244eaf9dd9989d2a6f11ce",
            title="test title",
            publishers="test publishers",
            category="test category"
            )
        bk.save()

        created_book = BookLog.objects.get(title="test title")
        return created_book

    def test_retrieve_book(self):
        created_book = self.create_book()
        retrieve_books_url = f"/api/frontend/books/{created_book.book_id}/"
        response = self.client.get(retrieve_books_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BorrowBookTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.duration = 4

    def create_book(self):
        bk = BookLog(
            book_id="8d41c47cb8244eaf9dd9989d2a6f11ce",
            title="test title",
            publishers="test publishers",
            category="test category"
            )
        bk.save()

        created_book = BookLog.objects.get(title="test title")
        return created_book

    def create_user(self):
        user = BookUser(
            email="test@test4.com",
            firstname="test firstname",
            lastname="test lastname")
        user.save()

        created_user = BookUser.objects.get(email="test@test4.com")
        return created_user

    def test_borrow_books(self):

        created_book = self.create_book()
        created_user = self.create_user()

        borrow_book_url = f"/api/frontend/books/borrow/{created_book.book_id}/"
        borrow_data = {
            "duration": self.duration,
            "bookuser": str(created_user.id)
        }
        response = self.client.post(borrow_book_url, json.dumps(borrow_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
