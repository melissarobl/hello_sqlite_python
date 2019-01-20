"""
sqlite3 context manager and try-except error handling

"""

import sqlite3


def create_table(db):
    try:
        with db:
            cur = db.cursor()
            cur.execute('create table phones (brand text, version int)')
    except sqlite3.Error as e:
        print(f'error creating table because {e}')


def add_test_data(db):

    try:
        with db:
            cur = db.cursor()
            cur.execute('insert into phones values ("Android", 5)')
            cur.execute('insert into phones values ("iPhone", 6)')

    except sqlite3.Error:
        print('Error adding rows')



def print_all_data(db):
    # Execute a query. Do not need a context manager, as no changes are being made to the DB
    try:
        cur = db.cursor()  # Need a cursor object to perform operations
        for row in cur.execute('select * from phones'):
            print(row)

    except sqlite3.Error as e:
        print(f'Error selecting data from phones table because {e}')


def delete_table(db):
    try:
        with db:
            cur = db.cursor()
            cur.execute('drop table phones')  # Delete table
    except sqlite3.Error as e:
        print(f'Error deleting phones table because {e}')


def main():
    db = None

    try:
        db = sqlite3.connect('my_first_db.db')
    except sqlite3.Error as e:
        print(f'Unable to connect to database because {e}.')

    if db is not None:
        create_table(db)
        add_test_data(db)
        print_all_data(db)
        delete_table(db)

        try:
            db.close()
        except sqlite3.Error:
            print(f'Error closing database because {e}')


if __name__ == '__main__':
    main()

