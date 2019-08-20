from unittest import TestCase
import peewee 

import database_config
database_config.database_path = 'database/test_books.db'

from model import Book
import bookstore 
from bookstore import BookError


class TestBookstore(TestCase):

    def setUp(self):
        database_config.database_path = 'database/test_books.db'
        self.clear_bookstore()


    def add_test_data(self):
        self.clear_bookstore()

        self.bk1 = Book(title='An Interesting Book', author='Ann Author', read=True)
        self.bk2 = Book(title='Booky Book Book', author='B. Bookwriter', read=False)
        self.bk3 = Book(title='Collection of words', author='Creative Creator')

        self.bk1.save()
        self.bk2.save()
        self.bk3.save()


    def clear_bookstore(self):
        bookstore.delete_all_books()


    def test_add_book_empty_store(self):        
        bk = Book(title='aa', author='aaa')
        bk.save()
        self.assertTrue(bookstore.exact_match(bk))
        self.assertEqual(1, bookstore.book_count())


    def test_add_book_store_with_books_in(self):
        self.add_test_data()
        book_count = bookstore.book_count()
        bk = Book(title='aa', author='bbbbb')
        bk.save()
        self.assertTrue(bookstore.exact_match(bk))
        self.assertEqual(book_count + 1, bookstore.book_count())


    def test_add_book_duplicate_errors(self):
        bk = Book(title='cc', author='ddddd')
        bk.save()
        with self.assertRaises(peewee.IntegrityError):
            bk_dupe = Book(title='cc', author='ddddd')
            bk_dupe.save()
       

    def test_add_book_duplicate_errors_case_insensitive(self):
        bk = Book(title='cc', author='ddddd')
        bk.save()
        with self.assertRaises(peewee.IntegrityError):
            bk_dupe = Book(title='Cc', author='dDdDd')
            bk_dupe.save()
       

    def test_get_book_by_id_found(self):
        self.add_test_data()
        result = bookstore.get_book_by_id(self.bk1.id)
        self.assertEqual(result, self.bk1)


    def test_get_book_by_id_not_found(self):
        # This test fails - student should fix 
        self.add_test_data()
        result = bookstore.get_book_by_id(-1)
        self.assertIsNone(result)


    def test_delete_book(self):
        self.add_test_data()
        count = bookstore.book_count()
        bookstore.delete_book(self.bk2)
        self.assertEqual(count - 1, bookstore.book_count())
        self.assertFalse(bookstore.exact_match(self.bk2))


    def test_delete_book_not_in_store_errors(self):
        self.add_test_data()
        bk = Book(title='Not in store', author='Not in store')
        with self.assertRaises(BookError):
            bookstore.delete_book(bk)


    def test_delete_book_empty_list_errors(self):
        bk = Book(title='Not in store', author='Not in store')
        with self.assertRaises(BookError):
            bookstore.delete_book(bk)


    def test_delete_all_books(self):
        bk1 = Book(title='Interesting Title', author='Author')
        bk2 = Book(title='Whatever', author='W. Whatever')
        bk1.save()
        bk2.save()

        bookstore.delete_all_books()
        self.assertEqual(0, bookstore.book_count())


    def test_delete_all_books_empty(self):
        bookstore.delete_all_books()
        self.assertEqual(0, bookstore.book_count())


    def test_count_books(self):
        self.add_test_data()
        count = bookstore.book_count()
        self.assertEqual(3, count)


    def test_set_read_book_read(self):
        self.add_test_data()
        self.bk1.read = True
        self.bk1.save()
       
        bk1_from_store = bookstore.get_book_by_id(self.bk1.id)
        self.assertTrue(bk1_from_store.read)


    def test_set_unread_book_read(self):
        self.add_test_data()
        self.bk2.read = True 
        self.bk2.save()
        
        bk2_from_store = bookstore.get_book_by_id(self.bk2.id)
        self.assertTrue(bk2_from_store.read)


    def test_set_read_book_unread(self):
        self.add_test_data()
      
        self.bk1.read = False
        self.bk1.save()

        bk1_from_store = bookstore.get_book_by_id(self.bk1.id)
        self.assertFalse(bk1_from_store.read)


    def test_set_unread_book_unread(self):
        self.add_test_data()
        self.bk2.read = False 
        self.bk2.save()

        bk2_from_store = bookstore.get_book_by_id(self.bk2.id)
        self.assertFalse(bk2_from_store.read)


    def test_get_all_books(self):
        self.add_test_data()
        self.assertCountEqual([self.bk1, self.bk2, self.bk3], bookstore.get_all_books())


    def test_is_book_in_store_present(self):
        self.add_test_data()
        self.assertTrue(bookstore.exact_match(self.bk1))
        self.assertTrue(bookstore.exact_match(self.bk2))
        self.assertTrue(bookstore.exact_match(self.bk3))


    def test_is_book_in_store_not_present(self):
        not_in_store = Book(title='aaaa', author='bbbb')
        self.add_test_data()
        self.assertFalse(bookstore.exact_match(not_in_store))


    def test_is_book_in_store_empty_list(self):
        self.clear_bookstore()
        not_in_store = Book(title='ccc', author='ddd')
        self.assertFalse(bookstore.exact_match(not_in_store))


    def test_search_book_author_match(self):
        self.add_test_data()
        self.assertCountEqual([self.bk1], bookstore.book_search('Ann'))


    def test_search_book_title_match(self):
        self.add_test_data()
        self.assertCountEqual([self.bk1, self.bk2], bookstore.book_search('Book'))


    def test_search_book_not_found(self):
        self.add_test_data()
        self.assertEqual([], bookstore.book_search('Not in list'))


    def test_search_book_empty_store(self):
        self.clear_bookstore()
        self.assertEqual([], bookstore.book_search('No book here'))


    def test_search_book_case_insensitive_title_match(self):
        self.add_test_data()
        self.assertCountEqual([self.bk1, self.bk2], bookstore.book_search('bOoK'))

 
    def test_search_book_case_insensitive_author_match(self):
        self.add_test_data()
        self.assertCountEqual([self.bk3], bookstore.book_search('cReAtOr'))


    def test_exact_match_found(self):
        self.add_test_data()
        bk = Book(title='Collection of words', author='Creative Creator')
        self.assertTrue(bookstore.exact_match(bk))


    def test_exact_match_not_found_author(self):
        self.add_test_data()
        bk = Book(title='Collection of words', author='Someone Else')
        self.assertFalse(bookstore.exact_match(bk))


    def test_exact_match_not_found_title(self):
        self.add_test_data()
        bk = Book(title='Collection of Stories', author='Creative Creator')
        self.assertFalse(bookstore.exact_match(bk))


    def test_exact_match_not_found_title_author(self):
        self.add_test_data()
        bk = Book(title='Collection of Songs', author='Beyonce')
        self.assertFalse(bookstore.exact_match(bk))


    def test_exact_match_not_found_empty_store(self):
        bk = Book(title='Whatever', author='Whatever')
        self.clear_bookstore()
        self.assertFalse(bookstore.exact_match(bk))


    def test_get_books_by_read_read(self):
        self.add_test_data()
        read_books = bookstore.get_books_by_read_value(True)
        self.assertCountEqual([self.bk1], read_books)


    def test_get_books_by_read_unread(self):
        self.add_test_data()
        read_books = bookstore.get_books_by_read_value(False)
        self.assertCountEqual([self.bk2, self.bk3], read_books)



