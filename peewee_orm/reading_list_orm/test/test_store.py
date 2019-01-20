from unittest import TestCase

import database_config
database_config.database_path = 'test_books.sqlite'


import bookstore as store
from bookstore import BookError

from model import Book


class TestBookstore(TestCase):


    def setUp(self):
        self.clear_bookstore()


    def add_test_data(self):
        self.bk1 = Book(title='An Interesting Book', author='Ann Author', read=True)
        self.bk2 = Book(title='Booky Book Book', author='B. Bookwriter', read=False)
        self.bk3 = Book(title='Collection of words', author='Creative Creator')

        self.clear_bookstore()

        store.add_book(self.bk1)
        store.add_book(self.bk2)
        store.add_book(self.bk3)


    def clear_bookstore(self):
        store.delete_all_books()


    def test_add_book_empty_store(self):
        store.delete_all_books()
        bk = Book(author='aa', title='aaa')
        store.add_book(bk)
        self.assertTrue(store.get_book_by_id(bk.id))
        self.assertEqual(1, store.book_count())


    def test_add_book(self):
        self.add_test_data()
        book_count = store.book_count()
        bk = Book(author='aa', title='bbbbb')
        store.add_book(bk)
        self.assertTrue(store.get_book_by_id(bk.id))
        self.assertEqual(book_count + 1, store.book_count())


    def test_add_book_duplicate_errors(self):
        bk = Book(title='aa', author='aaa')
        store.add_book(bk)
        with self.assertRaises(store.BookError):
            bk_dupe = Book(title='aa', author='aaa')
            store.add_book(bk_dupe)


    def test_delete_book(self):
        self.add_test_data()
        delete_id = self.bk2.id
        count = store.book_count()
        store.delete_book(delete_id)
        self.assertEqual(count - 1, store.book_count())
        self.assertIsNone(store.get_book_by_id(delete_id))


    def test_delete_book_not_in_store_errors(self):
        self.add_test_data()
        bk = Book('Not in store', 'Not in store')
        with self.assertRaises(BookError):
            store.delete_book(bk)


    def test_delete_book_empty_list_errors(self):
        self.clear_bookstore()
        bk = Book('Not in store', 'Not in store')
        with self.assertRaises(BookError):
            store.delete_book(bk)


    def test_delete_all_books(self):
        self.clear_bookstore()
        bk1 = Book(title='Not in store', author='Not in store')
        bk2 = Book(title='Whatever', author='Whatever')
        store.add_book(bk1)
        store.add_book(bk2)
        store.delete_all_books()
        self.assertEqual(0, store.book_count())


    def test_delete_all_books_empty(self):
        self.clear_bookstore()
        store.delete_all_books()
        self.assertEqual(0, store.book_count())


    def test_set_read_book_read(self):
        self.add_test_data()
        store.set_book_read(self.bk1.id, True)


    def test_set_unread_book_read(self):
        self.add_test_data()
        store.set_book_read(self.bk2.id, True)


    def test_set_read_book_unread(self):
        self.add_test_data()
        store.set_book_read(self.bk1.id, False)


    def test_set_unread_book_unread(self):
        self.add_test_data()
        store.set_book_read(self.bk2.id, False)


    def test_set_book_read_not_found_errors(self):
        bk = Book('Not in store', 'Not in store')
        with self.assertRaises(BookError):
            store.set_book_read(bk.id, True)


    def test_search_book_author_match(self):
        self.add_test_data()
        self.assertCountEqual([self.bk1], store.book_search('Ann'))


    def test_search_book_title_match(self):
        self.add_test_data()
        self.assertCountEqual([self.bk1, self.bk2], store.book_search('Book'))


    def test_search_book_not_found(self):
        self.add_test_data()
        self.assertListEqual([], store.book_search('Not in list'))


    def test_search_book_empty_store(self):
        self.clear_bookstore()
        self.assertListEqual([], store.book_search('Not in list'))


    def test_search_book_case_insensitive_title_match(self):
        self.add_test_data()
        self.assertCountEqual([self.bk1, self.bk2], store.book_search('bOoK'))


    def test_search_book_case_insensitive_author_match(self):
        self.add_test_data()
        self.assertCountEqual([self.bk3], store.book_search('cReAtOr'))


    def test_get_books_by_read_read(self):
        self.add_test_data()
        read_books = store.get_books_by_read_value(True)
        self.assertCountEqual([self.bk1], read_books)


    def test_get_books_by_read_unread(self):
        self.add_test_data()
        read_books = store.get_books_by_read_value(False)
        self.assertCountEqual([self.bk2, self.bk3], read_books)



