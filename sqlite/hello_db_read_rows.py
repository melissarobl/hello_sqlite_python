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
    print(row['brand'])  # The brand
    print(row['version'])  # The version


db.commit()  # Ask the database to save changes

db.close()  # And close
