import sqlite3

db = sqlite3.connect('my_first_db.db')  # Creates or opens database file

cur = db.cursor()  # Need a cursor object to perform operations

# Create a table
cur.execute('create table phones (brand text, version int)')

# Add some data
cur.execute('insert into phones values ("Android", 5)')
cur.execute('insert into phones values ("iPhone", 6)')

db.commit()  # Save changes

# Execute a query. Results are contained in cursor object
for row in cur.execute('select * from phones'):
    print(row)

cur.execute('drop table phones')  # Delete table

db.commit()  # Ask the database to save changes

db.close()


