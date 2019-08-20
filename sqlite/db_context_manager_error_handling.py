""" sqlite3 context manager and try-except error handling """

import sqlite3

database = 'phone_db.sqlite'

def create_table():
    try:
        with sqlite3.connect(database) as conn:
            conn.execute('create table phones (brand text, version int)')
    except sqlite3.Error as e:
        print(f'error creating table because {e}')
    finally:
        conn.close()


def add_test_data():

    try:
        with sqlite3.connect(database) as conn:
            conn.execute('insert into phones values ("Android", 5)')
            conn.execute('insert into phones values ("iPhone", 6)')
    except sqlite3.Error:
        print('Error adding rows')
    finally:
        conn.close()


def print_all_data():
    # Execute a query. Do not need a context manager, as no changes are being made to the db
    try:
        conn = sqlite3.connect(database) 
        for row in conn.execute('select * from phones'):
            print(row)
    except sqlite3.Error as e:
        print(f'Error selecting data from phones table because {e}')
    finally:
        conn.close()


def delete_table():
    try:
        with sqlite3.connect(database) as conn:
            conn.execute('drop table phones')
    except sqlite3.Error as e:
        print(f'Error deleting phones table because {e}')
    finally:
        conn.close()


def main():
    create_table()
    add_test_data()
    print_all_data()
    delete_table()



if __name__ == '__main__':
    main()

