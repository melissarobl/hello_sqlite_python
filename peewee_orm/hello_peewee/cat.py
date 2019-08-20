from peewee import *

# Which database?
db = SqliteDatabase('cats.sqlite')


# Create a Model class. This defines both the fields in the objects in your program
# and also the columns in the database. PeeWee maps between the two.

class Cat(Model):
    name = CharField()
    color = CharField()
    age = IntegerField()

    # Link this model to a particular database
    class Meta:
        database = db

    def __str__(self):
        return f'{self.name} is a {self.color} cat and is {self.age} years old'



# Connect to DB, and create tables that map to the model Cat.
# Can have many models, create_tables takes a list of model classes as the argument
db.connect()
db.create_tables([Cat])


# Create Cat objects and call save function to insert them into the database
print('\nCreate and save 3 cats')
zoe = Cat(name="Zoe", color='Ginger', age=3)
zoe.save()

holly = Cat(name="Holly", color='Tabby', age=7)
holly.save()

fluffy = Cat(name="Fluffy", color='Black', age=1)
fluffy.save()


# Can also insert many rows at once in a bulk insert,
# see documentation http://docs.peewee-orm.com/en/latest/peewee/querying.html#bulk-inserts


# Search - find all
print('\nFind all cats')
cats = Cat.select()
for cat in cats:
    print(cat)



# Update by modifying the model instance and saving
# If the model instance is already saved, then saving again will update the DB
zoe.age = 5
zoe.save()
print('\nZoe is now:', zoe)


# Updating in the database, if you don't have a model instance
# Watch the argument to the function - notice structure of update and where
# Remember to call execute()
# If you don't need to know how many rows were modified, simply call the Cat.update method.
rows_changed = Cat.update(color='Orange').where(Cat.color == 'Ginger').execute()
print('\nChanged ginger cats to orange which modified this many rows:', rows_changed)


# Insert another cat, same as before
print('\nAdd new cat')
buzz = Cat(name='Buzz', color='Gray', age='5')
buzz.save()
print(buzz)


# Select with query, all 5-year-old cats
print('\nAll 5 year old cats')
age_5 = Cat.select().where(Cat.age == 5)
for cat in age_5:
    print(cat)


# And finding by id (primary key)
buzz_id = buzz.id
buzz = Cat.get_by_id(buzz_id)
print(f'\nGet by ID {buzz_id} returns:', buzz)


# Find one or none, useful when only one result is expected
holly_again = Cat.get_or_none(Cat.name == 'Holly')
print('\nCat called Holly:', holly_again)


# Find one or none, no results
oscar = Cat.get_or_none(Cat.name == 'Oscar')
print('\nCat called Oscar:', oscar)  # None


# How many cats?
count = Cat.select().count()
print('\nThere are this many cats in the table:', count)


# Aggregate query, figuring out average age
print('\nAverage age of all cats:')
avg_age = Cat.select(fn.avg(Cat.age).alias('avg_age'))
for avg in avg_age:
    print('Average age', avg.avg_age)


# Delete Fluffy - delete rows that match a query
# If you don't need to know how many rows were changed, omit the rows_changed variable
print('\nDeleting Fluffy')
rows_deleted = Cat.delete().where(Cat.name == 'Fluffy').execute()
print('Rows deleted:', rows_deleted)


# Sorting. Notice Fluffy is deleted
print('\nCats, sorted by name')
for cat in Cat.select().order_by(Cat.name):
    print(cat)


# limit results
print('\nLimit results to a maximum of the first two rows')
only_two = Cat.select().limit(2)
for cat in only_two:
    print(cat)


# Can chain many methods
print('\nSelect 5-year-old cats, limit 2, sort by color ')
query = Cat.select().where(Cat.age == 5).order_by(Cat.color).limit(2)
for cat in query:
    print(cat)  # How many things printed?


print('\nDeleting all cats')
# Delete all cats
rows_deleted = Cat.delete().execute()
print('Rows deleted:', rows_deleted)


print('\nEverything in the database:')  # Nothing printed
for cat in Cat.select(Cat):
    print(cat)
