from unittest import TestCase
from model import Book, NO_ID


class TestBook(TestCase):

    def test_create_default_id(self):
        bk = Book('Title', 'Author')
        self.assertEqual(NO_ID, bk.id)


    def test_create_book_default_unread(self):
        bk = Book('Title', 'Author')
        self.assertFalse(bk.read)


    def test_string(self):
        bk = Book('AAAA', 'BBBB', True, 4)
        self.assertIn('4', str(bk))
        self.assertIn('AAAA', str(bk))
        self.assertIn('BBBB', str(bk))
        self.assertIn('You have read', str(bk))

