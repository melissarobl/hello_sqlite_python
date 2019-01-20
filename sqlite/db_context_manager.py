import sqlite3


# Add some data; using context manager
# Python 3 docs https://docs.python.org/3.6/library/sqlite3.html

with sqlite3.connect('my_first_db.db') as db:
    cur = db.cursor()
    cur.execute('insert into phones values ("Android", 5)')
    cur.execute('insert into phones values ("iPhone", 6)')

# Execute a query. Results are contained in cursor object returned from cur.execute
for row in cur.execute('select * from phones'):
    print(row)

with sqlite3.connect('my_first_db.db') as db:
    cur = db.cursor()
    cur.execute('drop table phones')  # Delete table

db.close()
