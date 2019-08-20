from unittest import TestCase

import database_config
database_config.database_path = 'database/test_books.db'

import bookstore
from model import Book

class TestBook(TestCase):

    def test_create_book_default_unread(self):
        bk = Book(title='Title', author='Author')
        self.assertFalse(bk.read)


    def test_string(self):
        bk = Book(author='AAAA', title='BBBB', read=True)
        self.assertIn('AAAA', str(bk))
        self.assertIn('BBBB', str(bk))
        self.assertIn('You have read', str(bk))


    def test_save_add_to_db(self):
        bk = Book(author='AAAA', title='BBBB', read=True)
        bk.save()
        self.assertIsNotNone(bk.id)  # Check book has ID
        
        self.assertEqual(bk, bookstore.get_book_by_id(bk.id))
        self.assertTrue(bookstore.exact_match(bk))
        

    def test_save_update_changes_to_db(self):
        
        bk = Book(author='CCC', title='DDD', read=True)
        bk.save()
        
        # Change some attributes and save 
        bk.author = 'EEE'
        bk.title = 'FFF'
        bk.read = False 

        bk.save() 
        
        # Check DB has same data as bk Book object 
        self.assertEqual(bk, bookstore.get_book_by_id(bk.id))
        self.assertTrue(bk, bookstore.exact_match(bk))
        

