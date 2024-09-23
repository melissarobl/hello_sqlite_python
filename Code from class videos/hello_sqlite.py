import sqlite3

db = 'lost_db.sqlite'


def create_table():
    with sqlite3.connect(db) as conn: #create context manager
        conn.execute('drop table products')  # delete table if already exists
        conn.execute('CREATE TABLE IF NOT EXISTS products(id int, name text)')
    conn.close()


def insert_example_data():
    with sqlite3.connect(db) as conn:
        conn.execute('INSERT INTO products values (1000, "hat")')
        conn.execute('INSERT INTO products values (2000, "JACKET")')
    conn.close()


def display_all_data():
    conn = sqlite3.connect(db) # do we need a context manager? No because we don't need to commit any changes
    results = conn.execute('SELECT * FROM products')
    print('All products: ')
    for row in results:
        print(row) # each row is a tuple object

    conn.close()

def display_one_product(product_name):
    conn = sqlite3.connect(db)
    results = conn.execute('SELECT * FROM products WHERE name like ?', (product_name,))
    first_row = results.fetchone()
    if first_row:
        print('Your product is: ', first_row) # upgrade to row factory later?
    else:
        print('not found')
    conn.close()


def create_new_product():
        new_id = int(input('enter new id: '))
        new_name = input ('enter new product name: ')

        with sqlite3.connect(db) as conn:
            conn.execute(f'INSERT INTO products VALUES (?, ?)', (new_id, new_name) )
            # conn.execute(f'INSERT INTO products VALUES ({new_id},"{new_name}")') --- don't use this format - too many crashes
        conn.close()


def update_product():
    updated_product = 'wool hat'
    update_id = 1001

    with sqlite3.connect(db) as conn:
         conn.execute('UPDATE products SET name = ? WHERE id = ?', (updated_product, update_id))
    conn.close()


def delete_product(product_name):
    with sqlite3.connect(db) as conn:
        conn.execute('DELETE FROM products WHERE name= ?', (product_name, ) )
    conn.close() # close connection - always needed - even with context manager


create_table()
insert_example_data()
display_all_data()
display_one_product('sweater')
display_one_product('coat')
create_new_product()
update_product()
delete_product('beret')
display_all_data()