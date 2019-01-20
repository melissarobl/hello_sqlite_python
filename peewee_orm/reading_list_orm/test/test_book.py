from unittest import TestCase


import database_config
database_config.database_path = 'test_books.sqlite'


from model import Book


class TestBook(TestCase):

    def test_create_book_default_unread(self):
        bk = Book('Title', 'Author')
        self.assertFalse(bk.read)


    def test_string(self):
        bk = Book(title='AAAA', author='BBBB', read=True, id=4)
        self.assertEqual('ID 4, Title: AAAA, Author: BBBB. You have read this book.', str(bk))

        bk = Book(title='AAAA', author='BBBB', read=False, id=4)
        self.assertEqual('ID 4, Title: AAAA, Author: BBBB. You have not read this book.', str(bk))
