"""
This program creates an SQLite database to hold information on the chainsaw juggling record holders. New jugglers can
be added, old jugglers can be deleted and number of catches can be edited. Record holders can be deleted completely as well.
A menu - you need to add the database and fill in the functions.
"""
import sqlite3

db = 'chainsaw_juggling.sqlite'


def main():
    # create database table OR set up Peewee model to create table
    create_table_of_chainsaw_juggling_data()
    add_data_to_chainsaw_juggling_db()

    menu_text = """
    1. Display all records
    2. Search by name
    3. Add new record
    4. Edit existing record
    5. Delete record 
    6. Quit
    """

    while True:
        print(menu_text)
        choice = input('Enter your choice: ')
        if choice == '1':
            display_all_records()
        elif choice == '2':
            search_by_name()
        elif choice == '3':
            add_new_record()
        elif choice == '4':
            edit_existing_record()
        elif choice == '5':
            delete_record()
        elif choice == '6':
            break
        else:
            print('Not a valid selection, please try again')


def create_table_of_chainsaw_juggling_data():
    try:
        with sqlite3.connect(db) as conn:
            conn.execute('CREATE TABLE IF NOT EXISTS chainsaw_juggling (Name TEXT, Country TEXT, Number_of_Catches INT)')
    except sqlite3.Error as e:
        print(f'Error creating table because {e}')
    conn.close()


def add_data_to_chainsaw_juggling_db():
    try:
        with sqlite3.connect(db) as conn:
            conn.execute('INSERT INTO chainsaw_juggling values ("Janne Mustonen", "Finland", 98)')
            conn.execute('INSERT INTO chainsaw_juggling values ("Ian Stewart", "Canada", 94)')
            conn.execute('INSERT INTO chainsaw_juggling values ("Aaron Gregg", "Canada", 88)')
            conn.execute('INSERT INTO chainsaw_juggling values ("Chad Taylor", "USA", 78)')
    except Exception as e:
        print(f'Error adding data because {e}')
    conn.close()


def display_all_records():
    with sqlite3.connect(db) as conn:
            all_records = conn.execute('SELECT * FROM chainsaw_juggling')
    print('Here are all the records: ')
    for record in all_records:
        print(record)
    conn.close()


def search_by_name():  # ask user for a name, and print the matching record if found. What should the program do if the name is not found?')
    juggler_search = (input('Enter the name of the juggler you are looking for: '))

    with sqlite3.connect(db) as conn:
        juggler_search_results = conn.execute('SELECT * FROM chainsaw_juggling WHERE UPPER(name) like ?', (juggler_search.upper(),  ))
        first_record = juggler_search_results.fetchone()
        if first_record:
            print('Here is the chainsaw juggler you are looking for: ', first_record)
        else:
            print(f'There is no record of {juggler_search} in the chainsaw juggler database.')
    conn.close()


def add_new_record():
    new_name = input('Enter the name of the new chainsaw juggler: ')
    new_country = input('Enter the name of their country: ')
    check_db_for_juggler_sql = 'SELECT * FROM chainsaw_juggling WHERE UPPER(name) = UPPER(?) AND UPPER(country) = UPPER(?)'
    add_new_juggler_sql = 'INSERT INTO chainsaw_juggling VALUES (?, ?, ?)'

    while True:
        try:
            new_number_of_catches = int(input('Enter the number of catches they have: '))
            break
        except ValueError:
            print('Please enter an integer for the number of catches.')
            continue
    try:
        with sqlite3.connect(db) as conn:
            existing_juggler_record = conn.execute(check_db_for_juggler_sql, (new_name, new_country, )).fetchone()
            if existing_juggler_record:
                print('This juggler already exists in the database.')
            else:
                conn.execute(add_new_juggler_sql, (new_name, new_country, new_number_of_catches))
                conn.commit()
                print('Added new chainsaw juggler.')
    except Exception as e:
        print(f'Error adding new record: {e}')
    finally:
        conn.close()


def edit_existing_record(): # You should be able to update the number of catches for a record holder. What if user wants to edit record that does not exist?
    juggler_search = (input('Enter the name of the juggler you need to update: '))
    juggler_by_name_sql = 'SELECT * FROM chainsaw_juggling WHERE UPPER(name) like ?'
    update_catches_sql = 'UPDATE chainsaw_juggling SET Number_of_Catches = ? WHERE UPPER(Name) = ?'

    with sqlite3.connect(db) as conn:
        juggler_search_results = conn.execute(juggler_by_name_sql, (juggler_search.upper(), )).fetchone()
        if juggler_search_results:
            update_catches = int(input(f'Enter the updated number of catches for {juggler_search}:'))
            conn.execute(update_catches_sql, (update_catches, juggler_search.upper(), ))
            conn.commit()
        else:
            print(f'There is no record of {juggler_search} in the chainsaw juggler database.')
    conn.close()


def delete_record(): # you should be able to delete a record, by record holder's name. What if user wants to delete record that does not exist?'
    juggler_to_delete = (input('Enter the name of the juggler to delete: '))
    juggler_search_sql = 'SELECT * FROM chainsaw_juggling WHERE UPPER(name) = ?'
    juggler_delete_sql = 'DELETE FROM chainsaw_juggling WHERE UPPER(name) = ?'

    with sqlite3.connect(db) as conn:
        juggler_search_results = conn.execute(juggler_search_sql, (juggler_to_delete.upper(),  ))
        first_record = juggler_search_results.fetchone()

        if first_record:
            conn.execute(juggler_delete_sql, (juggler_to_delete.upper(), ))
            conn.commit()
            print('This juggler information was deleted from the database: ', first_record)
        else:
            print(f'There is no record of juggler {juggler_to_delete} to delete.')
    conn.close()


if __name__ == '__main__':
    main()