import sqlite3



# Create a table

try:
    db = sqlite3.connect('my_first_db.db')  # Creates or opens database file
    cur = db.cursor()  # Need a cursor object to perform operations
    cur.execute('create table phones (brand text, version int)')

except sqlite3.Error:
    print('error creating table')

finally:
    db.close()


# Add some data; using context manager
# 'Connection objects can be used as context managers that automatically commit or rollback transactions. In the event of an exception, the transaction is rolled back; otherwise, the transaction is committed:'
# Python 3 docs https://docs.python.org/3.6/library/sqlite3.html

try:
    db = sqlite3.connect('my_first_db.db')  # Creates or opens database file
    cur = db.cursor()  # Need a cursor object to perform operations

    with db:
        cur.execute('insert into phones values ("Android", 5)')
        cur.execute('insert into phones values ("iPhone", 6)')

        # db.commit()  # Don't need - will be called automatically by the context manager if there's no error.
except sqlite3.Error as e:
    print('Error adding rows')
    print(e)
    #In the event of an error, transactions will be automatically rolled back.

finally:
    db.close()


# Execute a query. Do not need a context manager, as no changes are being made to the DB
try:
    db = sqlite3.connect('my_first_db.db')  # Creates or opens database file
    cur = db.cursor()  # Need a cursor object to perform operations

    for row in cur.execute('select * from phones'):
        print(row)

except sqlite3.Error as e:
    print('Error selecting data from phones table')
    print(e)

finally:
    db.close()

# Delete table. Use context manager

try:
    db = sqlite3.connect('my_first_db.db')  # Creates or opens database file
    cur = db.cursor()  # Need a cursor object to perform operations
    with db:
        cur.execute('drop table phones')  # Delete table
        #db.commit()  # Not needed, context manager will commit automatically
except sqlite3.Error as e:
    print('Error deleting phones table')
    print(e)
finally:
    db.close()
