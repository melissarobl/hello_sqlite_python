from model import Book
from peewee import *
from peewee import IntegrityError


def delete_book(book_id):
    """ Removes book from store. Raises BookError if book not in store. 
    :param book_id the book model id to delete """
    rows_deleted = Book.delete().where(Book.id == book_id).execute()
    if not rows_deleted:
        raise BookError('Tried to delete book that doesn\'t exist')


def add_book(book):
    """ Adds book to store. Should error if a book with exact author and title is already in the store.
    :param book the book to add
    :raises BookError if book with same author and title is already in list."""
    try:
        book.save()
    except IntegrityError as e:
        raise BookError('Duplicate Book') from e


def delete_all_books():
    """ Clears the book list """
    Book.delete().execute()


def set_book_read(id, read):
    """ Changes whether a book has been read or not
    :param id the ID of the book to change the read status
    :param read True for book has been read, False otherwise
    :raises BookError if book with given ID is not in the database
    """

    rows_modified = Book.update(read=read).where(Book.id == id).execute()
    if not rows_modified:
        raise BookError(f'Book with id {id} not found')


def get_book_by_id(book_id):
    """ Searches list for Book with given ID,
    :param book_id the ID to search for
    :returns the book, if found, or None if book not found.
    """
    return Book.get_or_none(Book.id == book_id)


def book_search(term):
    """ Searches the store for books whose author or title contain a search term.
    Makes partial matches, so a search for 'Row' will match a book with author='JK Rowling'; a book with title='Rowing For Dummies'
    :param term the search term
    :returns a list of books with author or title that match the search term.
    """
    query = Book.select().where((Book.title.contains(term)) | (Book.author.contains(term)))
    return list(query)


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
    query = Book.select().where(Book.read == read)
    return list(query)


def get_all_books():
    """ :returns entire booklist """
    query = Book.select()
    return list(query)


class BookError(Exception):
    """ For BookStore errors. """
    pass
