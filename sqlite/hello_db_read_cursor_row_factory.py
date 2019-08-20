import sqlite3

conn = sqlite3.connect('first_db.sqlite')  # Creates or opens database file
conn.row_factory = sqlite3.Row  # Upgrade row_factory

# Create a table
conn.execute('create table if not exists phones (brand text, version integer)')

# Add some data
conn.execute('insert into phones values ("Android", 5)')
conn.execute('insert into phones values ("iPhone", 6)')

conn.commit()  # Finalize updates 

for row in conn.execute('select * from phones'):
    print(row['brand'])
    print(row['version'])

conn.close()  # And close


