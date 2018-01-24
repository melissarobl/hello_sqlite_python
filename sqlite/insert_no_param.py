import sqlite3

db = sqlite3.connect('my_first_db.db')  # Creates or opens database file

cur = db.cursor()  # Need a cursor object to perform operations

# Create a table if not exists...
cur.execute('create table if not exists phones (brand text, version integer)')

# Ask user for information for a new phone
brand = input('Enter brand of phone: ')
version = int(input('Enter version of phone (as an integer): '))

# No parameters. A format string will just build a string from
# the brand and version variables, and is still vulnerable to SQL injections
cur.execute('insert into phones values ("%s", %d)' % (brand, version))

# Fetch and display all data. Results stored in the cursor object
cur.execute('select * from phones')

for row in cur:
    print(row)

db.commit()  # Ask the database to save changes

db.close()

# TODO error handling!
