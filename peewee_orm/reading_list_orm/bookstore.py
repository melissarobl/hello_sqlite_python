from model import Book
from peewee import *


    
def delete_book(book):
    """ Removes book from store. Raises BookError if book not in store. 
    :param book the book model to delete """
    rows_deleted = book.delete_instance()
    if not rows_deleted:
        raise BookError('Tried to delete book that doesn\'t exist')



def add_book(book):
    """ Adds book to store. Should error if a book with exact author and title is already in the store.
    :param book the book to add
    :raises BookError if book with same author and title is already in list."""

    book.save()
    


def delete_all_books():
    """ Clears the book list """

    Book.delete().execute()



def set_book_read(id, read):
    """ Changes whether a book has been read or not
    :param id the ID of the book to change the read status
    :param read True for book has been read, False otherwise
    :raises BookError if book with given ID is not in the database
    """

    book = Book.get_or_none(id == id)
    if not book:
        raise BookError('Tried to modify book that doesn\'t exist')

    book.read = read
    book.save()



def get_book_by_id(id):
    """ Searches list for Book with given ID,
    :param id the ID to search for
    :returns the book, if found, or None if book not found.
    """

    return Book.get_or_none(id == id)



def book_search(term):
    """ Searches the store for books whose author or title contain a search term.
    Makes partial matches, so a search for 'Row' will match a book with author='JK Rowling'; a book with title='Rowing For Dummies'
    :param term the search term
    :returns a list of books with author or title that match the search term.
    """

    search = f'%{term.upper}%'
    return Book.select().where( (Book.author == search) | (Book.title == search))



def book_count():
    """ Counts the books in store.
    :returns the number of books .
    """

    return Book.select().count()



def get_books_by_read_value(read):
    """ Get a list of books that have been read, or list of books that have not been read.
    :param read True for books that have been read, False for books that have not been read
    :returns all books with the read value.
    """
    return Book.select().where(Book.read == read)



def get_all_books():
    """ :returns entire booklist """
    return Book.select()



class BookError(Exception):
    """ For BookStore errors. """
    pass
