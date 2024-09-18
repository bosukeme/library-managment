import uuid
from django.shortcuts import get_object_or_404
import logging
from .models import BookUserLog, BorrowBookLog, Book

logger = logging.getLogger('backend')


class ReceiveMessage:
    @classmethod
    def add_user_userlog(cls, data):

        if data['firstname'] != "test firstname":
            book_user_log = BookUserLog(
                    user_id=data['id'],
                    email=data['email'],
                    firstname=data['firstname'],
                    lastname=data['lastname'],
                )

            book_user_log.save()

            logger.info(f"book user {book_user_log.user_id} saved to log")

    @classmethod
    def add_borrow_book_log(cls, data):

        book_id = uuid.UUID(data['book_id'])
        book = get_object_or_404(Book, id=book_id)

        user_id = data['bookuser_id']
        book_user = get_object_or_404(BookUserLog, user_id=user_id)

        borrow_log = BorrowBookLog(
            borrow_id=uuid.UUID(data['id']),
            bookuser=book_user,
            book=book,
            duration=data['duration'],
        )
        borrow_log.save()

        book.isBorrowed = True
        book.save()

        logger.info(f"book borrow {borrow_log.borrow_id} saved to log")


def sort_receive_message(data):

    if data['type'] == "create_user":
        ReceiveMessage.add_user_userlog(data)
    elif data['type'] == "borrow_book":
        ReceiveMessage.add_borrow_book_log(data)
    else:
        raise AssertionError("Wrong type sent")
