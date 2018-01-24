import sqlite3

db = sqlite3.connect('my_first_db.db')  # Creates or opens database file
db.row_factory = sqlite3.Row  # Upgrade row_factory
cur = db.cursor()

## Add data here...

for row in cur.execute('select * from phones'):
    print(row['brand'])
    print(row['version'])


db.commit()  # Ask the database to save changes if needed
db.close()  # And close
