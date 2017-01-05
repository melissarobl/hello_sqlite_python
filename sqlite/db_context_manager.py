import sqlite3

db = sqlite3.connect('my_first_db.db')  # Creates or opens database file

cur = db.cursor()  # Need a cursor object to perform operations

# Create a table
cur.execute('create table phones (brand text, version int)')

# Add some data; using context manager
# Python 3 docs https://docs.python.org/3.6/library/sqlite3.html

with db:
    cur.execute('insert into phones values ("Android", 5)')
    cur.execute('insert into phones values ("iPhone", 6)')

    # db.commit()  # Don't need - will be called automatically by the context manager

# Execute a query. Results are contained in cursor object returned from cur.execute
for row in cur.execute('select * from phones'):
    print(row)

with db:
    cur.execute('drop table phones')  # Delete table
    #db.commit()  # Not needed, context manager commits if transaction was successful

db.close()
