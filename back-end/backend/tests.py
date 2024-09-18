import json
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from .models import Book, BookUserLog, BorrowBookLog


class CreateBookTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.data = {
            "title": "test title",
            "publishers": "test publishers",
            "category": "test category",

        }
        self.create_book_url = "/api/backend/books/"

    def test_create_book(self):
        response = self.client.post(self.create_book_url, json.dumps(self.data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)

        created_book = Book.objects.get(title=self.data['title'])
        self.assertEqual(created_book.title, "test title")

    def test_create_without_title(self):
        data = self.data
        data.pop('title')

        response = self.client.post(self.create_book_url, json.dumps(self.data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Book.objects.count(), 0)

    def test_create_without_publishers(self):
        data = self.data
        data.pop('publishers')

        response = self.client.post(self.create_book_url, json.dumps(self.data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Book.objects.count(), 0)

    def test_create_without_category(self):
        data = self.data
        data.pop('category')

        response = self.client.post(self.create_book_url, json.dumps(self.data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Book.objects.count(), 0)


class DeleteBookTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.data = {
            "title": "test title",
            "publishers": "test publishers",
            "category": "test category",

        }
        self.create_book_url = "/api/backend/books/"

    def create_book(self):
        self.client.post(self.create_book_url, json.dumps(self.data), content_type='application/json')
        created_book = Book.objects.get(title=self.data['title'])

        return created_book

    def test_delete_book_success(self):
        book = self.create_book()
        book_id = book.id

        delete_book_url = f"/api/backend/books/{book_id}/"

        response = self.client.delete(delete_book_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_delete_book_failure(self):
        self.create_book()
        book_id = "3fa85f64-5717-4562-b3fc-2c963f66afa6"

        delete_book_url = f"/api/backend/books/{book_id}/"

        response = self.client.delete(delete_book_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Book.objects.count(), 1)


class ListUserTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.userdata = {
            "email": "test@test.com",
            "firstname": "test firstname",
            "lastname": "test lastname",
            "user_id": "0d41c47cb8244eaf9dd9989d2a6f11ce"
        }
        self.user_url = "/api/backend/users/"

    def create_user(self):
        bk_user = BookUserLog(
                email=self.userdata['email'],
                firstname=self.userdata['firstname'],
                lastname=self.userdata['lastname'],
                user_id=self.userdata['user_id'],
                )
        bk_user.save()

    def test_list_book_users(self):
        self.create_user()
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BookUserLog.objects.count(), 1)


class ListUserBookBorrowTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.userdata = {
            "email": "test@test.com",
            "firstname": "test firstname",
            "lastname": "test lastname",
            "user_id": "0d41c47cb8244eaf9dd9989d2a6f11ce"
        }

        self.bookdata = {
            "title": "test title",
            "publishers": "test publishers",
            "category": "test category",
        }

        self.duration = 4
        self.user_borrow_url = "/api/backend/borrowed-books/"

    def create_user(self):
        bk_user = BookUserLog(
                email=self.userdata['email'],
                firstname=self.userdata['firstname'],
                lastname=self.userdata['lastname'],
                user_id=self.userdata['user_id'],
                )
        bk_user.save()

        book_user = BookUserLog.objects.get(email=self.userdata['email'])
        return book_user

    def create_book(self):
        self.create_book_url = "/api/backend/books/"
        response = self.client.post(self.create_book_url, json.dumps(self.bookdata), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_book = Book.objects.get(title=self.bookdata['title'])
        return created_book

    def borrow_book(self):
        created_book = self.create_book()
        created_user = self.create_user()

        boorow_book_log = BorrowBookLog(
            borrow_id="9d41c47cb8244eaf9dd9989d2a6f11ce",
            bookuser=created_user,
            book=created_book,
            duration=self.duration
        )

        boorow_book_log.save()

        created_borrow_obj = BorrowBookLog.objects.get(book=created_book.id)
        return created_borrow_obj

    def test_list_user_borrowed_books(self):
        self.borrow_book()
        response = self.client.get(self.user_borrow_url)
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BorrowBookLog.objects.count(), 1)
        self.assertEqual(response_data[0]['book_user'], self.userdata['firstname'])


class ListBookUnavailableTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.userdata = {
            "email": "test@test.com",
            "firstname": "test firstname",
            "lastname": "test lastname",
            "user_id": "0d41c47cb8244eaf9dd9989d2a6f11ce"
        }

        self.bookdata = {
            "title": "test title",
            "publishers": "test publishers",
            "category": "test category",
        }

        self.duration = 4

        self.user_unavailable_borrow_url = "/api/backend/unavailable-borrowed-books/"

    def create_user(self):
        bk_user = BookUserLog(
                email=self.userdata['email'],
                firstname=self.userdata['firstname'],
                lastname=self.userdata['lastname'],
                user_id=self.userdata['user_id'],
                )
        bk_user.save()

        book_user = BookUserLog.objects.get(email=self.userdata['email'])
        return book_user

    def create_book(self):
        self.create_book_url = "/api/backend/books/"
        response = self.client.post(self.create_book_url, json.dumps(self.bookdata), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_book = Book.objects.get(title=self.bookdata['title'])
        return created_book

    def borrow_book(self):
        created_book = self.create_book()
        created_user = self.create_user()

        boorow_book_log = BorrowBookLog(
            borrow_id="9d41c47cb8244eaf9dd9989d2a6f11ce",
            bookuser=created_user,
            book=created_book,
            duration=self.duration
        )

        boorow_book_log.save()

        created_borrow_obj = BorrowBookLog.objects.get(book=created_book.id)
        return created_borrow_obj

    def test_list_unavailable_borrowed_books(self):
        self.borrow_book()
        response = self.client.get(self.user_unavailable_borrow_url)
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BorrowBookLog.objects.count(), 1)
        self.assertEqual(response_data[0]['duration'], self.duration)
