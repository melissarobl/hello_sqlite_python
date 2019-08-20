import sqlite3

# Creates or opens connection to db file
conn = sqlite3.connect('first_db.sqlite')

# Create a table
conn.execute('create table if not exists phones (brand text, version integer)')

# Add some data
conn.execute('insert into phones values ("Android", 5)')
conn.execute('insert into phones values ("iPhone", 6)')

conn.commit()  # Finalize updates 

# Execute a query. execute() returns a cursor
# Can use the cursor in a loop to read each row in turn
for row in conn.execute('select * from phones'):
    print(row)


# If you know you don't have too many rows, can fetch all
# Returns a list of row objects 
cur = conn.execute('select * from phones')
all_phones = cur.fetchall()
print(all_phones)


# If you want to fetch one row, use fetchone
# Useful if you know you only expect one row 
cur = conn.execute('select * from phones')
first_phone = cur.fetchone()  
# If there are more rows, close the cursor, or read all of the rest of the rows, 
# or close your DB connection before attempting any more DB operations
# Otherwise, the cursor retains a lock on the table, and you'll get a 'table is locked' error 
cur.close() 


conn.execute('drop table phones')  # Delete table

conn.commit()  # Ask the database to save changes - don't forget!

conn.close()  # And close connection.




