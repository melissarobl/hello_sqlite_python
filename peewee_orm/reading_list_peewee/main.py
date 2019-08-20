""" Program to create and manage a list of books that the user wishes to read, and books that the user has read. """
import peewee 

import bookstore
from bookstore import Book
from menu import Menu
import ui


def main():

    menu = create_menu()

    while True:
        choice = ui.display_menu_get_choice(menu)
        action = menu.get_action(choice)
        action()
        if choice == 'Q':
            break


def create_menu():
    menu = Menu()
    menu.add_option('1', 'Add Book', add_book)
    menu.add_option('2', 'Search For Book', search_book)
    menu.add_option('3', 'Show Unread Books', show_unread_books)
    menu.add_option('4', 'Show Read Books', show_read_books)
    menu.add_option('5', 'Show All Books', show_all_books)
    menu.add_option('6', 'Change Book Read Status', change_read)
    menu.add_option('Q', 'Quit', quit_program)

    return menu


def add_book():
    new_book = ui.get_book_info()
    try:
        new_book.save()
    except peewee.IntegrityError:
        ui.message('Error, book already exists in the database')    


def show_read_books():
    read_books = bookstore.get_books_by_read_value(True)
    ui.show_books(read_books)


def show_unread_books():
    unread_books = bookstore.get_books_by_read_value(False)
    ui.show_books(unread_books)


def show_all_books():
    books = bookstore.get_all_books()
    ui.show_books(books)


def search_book():
    search_term = ui.ask_question('Enter search term, will match partial authors or titles.')
    matches = bookstore.book_search(search_term)
    ui.show_books(matches)


def change_read():
    book_id = ui.get_book_id()
    book = bookstore.get_book_by_id(book_id)  
    if not book:
        ui.message('Book not found')
        return
    new_read = ui.get_read_value()     
    book.read = new_read 
    book.save()
    

def quit_program():
    ui.message('Thanks and bye!')


if __name__ == '__main__':
    main()
