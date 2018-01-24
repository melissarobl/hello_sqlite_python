import sqlite3

db = sqlite3.connect('my_first_db.db')  # Creates or opens database file

cur = db.cursor()  # Need a cursor object to perform operations

# Create a table
cur.execute('create table if not exists phones (brand text, version integer)')

# Add some data
cur.execute('insert into phones values ("Android", 5)')
cur.execute('insert into phones values ("iPhone", 6)')

db.commit()  # Save changes. Don't forget this!

# Execute a query. Results are contained in cursor object
# One approach - treat cursor as iterator
for row in cur.execute('select * from phones'):
    print(row)

# Or, use fetchall() to get all rows as a list
all_data = cur.execute('select * from phones').fetchall();
print(all_data)

# Or, use fetchone() to get one row at a time
# fetchone() returns None when there are no more rows to read
row = cur.execute('select * from phones').fetchone();
print(row)

db.commit()  # Ask the database to save changes

db.close()  # And close connection.
