import sqlite3

from model import Book

database_file = 'books.sqlite'


class BookStore:

    """ Singleton class to hold and manage a database of books """

    instance = None

    class __BookStore:
        def __init__(self):
            self._db = sqlite3.connect(database_file)
            self._db.row_factory = sqlite3.Row

            with self._db as db:
                cur = db.cursor()
                cur.execute('CREATE TABLE IF NOT EXISTS books (title TEXT, author TEXT, read INT, UNIQUE (title, author))')


        def add_book(self, book):
            """ Adds book to store. Should error if a book with exact author and title is already in the store.
            :param book the book to add
            :raises BookError if book with same author and title is already in list."""

            try:
                with self._db as db:
                    cur = db.cursor()
                    cur.execute('INSERT INTO books values (?, ?, ?)', (book.title, book.author, book.read))
                    book.id = cur.lastrowid
            except sqlite3.IntegrityError:
                raise BookError('This book is already in the database')
            except sqlite3.Error as e:
                raise BookError(f'Error adding book {book}') from e


        def delete_book(self, book):
            """ Removes book from store. Raises BookError if book not in store. """
            try:
                with self._db as db:
                    cur = db.cursor()
                    cur.execute('DELETE FROM books WHERE rowid = ?', (book.id, ))
                    if not cur.rowcount:
                        raise BookError('Tried to delete book that doesn\'t exist')
            except sqlite3.Error as e:
                raise BookError('Error deleting book') from e


        def delete_all_books(self):
            """ Clears the book list """
            try:
                with self._db as db:
                    cur = db.cursor()
                    cur.execute('DELETE FROM books')
            except sqlite3.Error as e:
                raise BookError('Error deleting all books') from e


        def set_book_read(self, id, read):
            """ Changes whether a book has been read or not
            :param id the ID of the book to change the read status
            :param read True for book has been read, False otherwise
            :raises BookError if book with given ID is not in the database
            """

            try:
                with self._db as db:
                    cur = db.cursor()
                    cur.execute('UPDATE books SET read = ? WHERE rowid = ?', (read, id))
                    if not cur.rowcount:
                        raise BookError('Tried to modify book that doesn\'t exist')
            except sqlite3.Error as e:
                raise BookError(f'Error setting book {id} to read={read}') from e



        def get_book_by_id(self, id):
            """ Searches list for Book with given ID,
            :param id the ID to search for
            :returns the book, if found, or None if book not found.
            """

            try:
                cur = self._db.cursor()
                results = cur.execute('SELECT rowid, * FROM books WHERE rowid = ?', (id, ))
                book_row = results.fetchone()
                return self._row_to_book(book_row)
            except sqlite3.Error as e:
                raise BookError(f'Error getting book ID {id}') from e


        def book_search(self, term):
            """ Searches the store for books whose author or title contain a search term.
            Makes partial matches, so a search for 'Row' will match a book with author='JK Rowling'; a book with title='Rowing For Dummies'
            :param term the search term
            :returns a list of books with author or title that match the search term.
            """

            try:
                cur = self._db.cursor()
                search = f'%{term.upper()}%'
                cur.execute('SELECT rowid, * FROM books WHERE UPPER(title) like ? OR UPPER(author) like ?', (search, search))
                return self._cursor_to_booklist(cur)
            except sqlite3.Error as e:
                raise BookError(f'Error searching for books with search term {term}') from e


        def book_count(self):
            """ Counts the books in store.
            :returns the number of books .
            """

            try:
                cur = self._db.cursor()
                cur.execute('SELECT COUNT(*) FROM books')
                return cur.fetchone()[0]
            except sqlite3.Error as e:
                raise BookError(f'Error searching for books with search term {term}') from e


        def get_books_by_read_value(self, read):
            """ Get a list of books that have been read, or list of books that have not been read.
            :param read True for books that have been read, False for books that have not been read
            :returns all books with the read value.
            """
            try:
                cur = self._db.cursor()
                cur.execute('SELECT rowid, * FROM books WHERE read = ?', (read,))
                return self._cursor_to_booklist(cur)

            except sqlite3.Error as e:
                raise BookError(f'Error getting books with read = {read}') from e


        def get_all_books(self):
            """ :returns entire booklist """

            try:
                cur = self._db.cursor()
                cur.execute('SELECT rowid, * FROM books')
                return self._cursor_to_booklist(cur)

            except sqlite3.Error as e:
                raise BookError('Error getting all books') from e


        # def close(self):
        #     self._db.close()


        def _row_to_book(self, row):
            if not row:
                return None
            book = Book(row['title'], row['author'], row['read'] != 0, row['rowid'])

            return book


        def _cursor_to_booklist(self, cur):
            return [self._row_to_book(row) for row in cur]


    def __new__(cls):
        if not BookStore.instance:
            BookStore.instance = BookStore.__BookStore()
        return BookStore.instance


    def __getattr__(self, name):
        return getattr(self.instance, name)


    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)



class BookError(Exception):
    """ For BookStore errors. """
    pass
