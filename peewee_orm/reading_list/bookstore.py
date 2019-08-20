from model import Book
from peewee import fn
        
def delete_book(book):
    """ Removes book from store. Raises BookError if book not in store. 
    :param book the Book to delete """

    rows_deleted = Book.delete().where(Book.id == book.id).execute()
    if not rows_deleted:
        raise BookError('Tried to delete book that doesn\'t exist')


def delete_all_books():
    """ Deletes all books from database """
    Book.delete().execute()


def get_book_by_id(book_id):
    """ Searches list for Book with given ID,
    :param id the ID to search for
    :returns the book, if found, or None if book not found.
    """
    return Book.get_or_none(Book.id == book_id)


def exact_match(book):
    search = Book.get_or_none( (Book.title == book.title) & (Book.author == book.author) )
    return search is not None  


def book_search(term):
    """ Searches the store for books whose author or title contain a search term. Case insensitive.
    Makes partial matches, so a search for 'row' will match a book with author='JK Rowling' and a book with title='Rowing For Dummies'
    :param term the search term
    :returns a list of books with author or title that match the search term. The list will be empty if there are no matches.
    """

    query = Book.select().where( ( fn.LOWER(Book.title).contains(term.lower() ) ) | (fn.LOWER(Book.author).contains(term.lower())))
    return list(query)


def get_books_by_read_value(read):
    """ Get a list of books that have been read, or list of books that have not been read.
    :param read True to find all books that have been read, False to find all books that have not been read
    :returns all books with the read value.
    """
    
    query = Book.select().where(Book.read == read)
    return list(query)


def get_all_books():
    """ :returns entire book list """

    query = Book.select()
    return list(query)


def book_count():
    """ :returns the number of books in the store """
    
    return Book.select().count()



class BookError(Exception):
    """ For BookStore errors. """
    pass
