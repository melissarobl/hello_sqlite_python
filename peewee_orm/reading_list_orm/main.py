""" Program to create and manage a list of books that the user wishes to read, and books that the user has read. """

import bookstore as store
from bookstore import BookError
from menu import Menu
import ui

QUIT = 'Q'


def main():

    menu = create_menu()

    while True:
        choice = ui.display_menu_get_choice(menu)
        action = menu.get_action(choice)
        action()
        if choice == QUIT:
            break


def create_menu():
    menu = Menu()
    menu.add_option('1', 'Add Book', add_book)
    menu.add_option('2', 'Search For Book', search_book)
    menu.add_option('3', 'Show Unread Books', show_unread_books)
    menu.add_option('4', 'Show Read Books', show_read_books)
    menu.add_option('5', 'Show All Books', show_all_books)
    menu.add_option('6', 'Change Book Read Status', change_read)
    menu.add_option('7', 'Delete Book', delete_book)
    menu.add_option(QUIT, 'Quit', quit_program)

    return menu


def add_book():
    new_book = ui.get_book_info()
    try:
        store.add_book(new_book)
        ui.message('Book added')
    except BookError as e:
        ui.message(e)


def show_read_books():
    read_books = store.get_books_by_read_value(True)
    ui.show_books(read_books)


def show_unread_books():
    unread_books = store.get_books_by_read_value(False)
    ui.show_books(unread_books)


def show_all_books():
    books = store.get_all_books()
    ui.show_books(books)


def search_book():
    search_term = ui.ask_question('Enter search term, will match partial authors or titles.')
    matches = store.book_search(search_term)
    ui.show_books(matches)


def change_read():
    book_id = ui.get_book_id()
    new_read = ui.get_read_value()
    try:
        store.set_book_read(book_id, new_read)
        ui.message('Updated.')
    except BookError as e:
        ui.message(e)


def delete_book():
    book_id = ui.get_book_id()
    try:
        store.delete_book(book_id)
        print('Book deleted')
    except BookError as e:
        ui.message(e)


def quit_program():
    # store.close()
    ui.message('Thanks and bye!')


