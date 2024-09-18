import uuid
import logging
from .models import BookLog

logger = logging.getLogger('frontend')


class ReceiveMessage:
    @classmethod
    def add_book_booklog(cls, data):

        if data['title'] != "test title":
            book_log = BookLog(
                    book_id=uuid.UUID(data['id']),
                    title=data['title'],
                    publishers=data['publishers'],
                    category=data['category'],
                    isBorrowed=data['isBorrowed'],
                )

            book_log.save()
            logger.info(f"book {book_log.book_id} saved to log")

    @classmethod
    def delete_book_booklog(cls, data):

        try:
            if data['title'] != "test title":
                book_log = BookLog.objects.get(title=data['title'])
                book_log.delete()
                logger.info(f"book {book_log.book_id} deleted from log")
        except BookLog.DoesNotExist:
            pass


def sort_receive_message(data):

    if data['type'] == "create":
        ReceiveMessage.add_book_booklog(data)
    elif data['type'] == "delete":
        ReceiveMessage.delete_book_booklog(data)
    else:
        raise AssertionError("Wrong type sent")
