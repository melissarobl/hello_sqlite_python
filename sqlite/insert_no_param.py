import sqlite3

conn = sqlite3.connect('my_first_db.db')  # Creates or opens database file

# Create a table if not exists...
conn.execute('create table if not exists phones (brand text, version integer)')

# Ask user for information for a new phone
brand = input('Enter brand of phone: ')
version = int(input('Enter version of phone (as an integer): '))

# No parameters. A format string will just build a string from
# the brand and version variables, and is still vulnerable to SQL injections
conn.execute('insert into phones values ("%s", %d)' % (brand, version))
# Format strings are just as bad!
# cur.execute(f'insert into phones values ("{brand}", {version})')  # Don't do this either!

conn.commit()  # Ask the database to save changes

# Fetch and display all data. Results stored in the cursor object
cur = conn.execute('select * from phones')

for row in cur:
    print(row)

conn.close()

