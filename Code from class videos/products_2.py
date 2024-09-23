import sqlite3

# validation errors, row id -- row id is an automatically generated primary key. Starts at 1.

db = 'products.sqlite'

with sqlite3.connect(db) as conn:
    conn.execute('CREATE TABLE IF NOT EXISTS products (product_id INTEGER PRIMARY KEY, name TEXT UNIQUE, quantity INT)') # constraints in input of text and quantity
conn.close()

name = 'gloves'
quantity = 1

try:
    with sqlite3.connect(db) as conn:
        conn.execute('INSERT INTO products ( name, quantity) VALUES (?, ?)', (name, quantity) )
    conn.close()
except Exception as e:
    print('Error inserting ', e)

conn = sqlite3.connect(db)
results = conn.execute('SELECT rowid, * FROM products') # rowid is not included in *, so you have to request it specifically if not in other query as above

for row in results:
    print(row)

print('end of program!')