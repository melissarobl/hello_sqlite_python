import sqlite3


# Using context manager

with sqlite3.connect('my_first_db.db') as conn:
    conn.execute('create table if not exists phones (brand text, version integer)')


with sqlite3.connect('my_first_db.db') as conn:
    conn.execute('insert into phones values ("Android", 5)')
    conn.execute('insert into phones values ("iPhone", 6)')
    # No commit statement needed 

    # Execute a query. Results are contained in cursor object returned from cur.execute
    for row in conn.execute('select * from phones'):
        print(row)


with sqlite3.connect('my_first_db.db') as conn:
    conn.execute('drop table phones')  # Delete table

conn.close()


