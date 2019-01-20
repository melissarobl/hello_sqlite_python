from peewee import *

db = SqliteDatabase('cats.sqlite')


class Cat(Model):
    name = CharField()
    color = CharField()
    age = IntegerField()

    class Meta:
        database = db

    def __str__(self):
        return f'{self.name} is a {self.color} cat and is {self.age} years old'


db.connect()
db.create_tables([Cat])

print('\nCreate and save 3 cats')
zoe = Cat(name="Zoe", color='Ginger', age=3)
zoe.save()

holly = Cat(name="Holly", color='Tabby', age=7)
holly.save()

mog = Cat(name="Mog", color='Black', age=1)
mog.save()


print('\nFind all cats')
# Search - find all
cats = Cat.select()
for cat in cats:
    print(cat)

# Delete Mog
print('\nDeleting Mog')
Cat.delete().where(Cat.name == 'Mog').execute()

# Update by modifying the model instance and saving
zoe.age = 5
zoe.save()
print('\nZoe is now:', zoe)


# Insert another cat
print('\nAdd new cat')
buzz = Cat(name='Buzz', color='Gray', age='5')
buzz.save()
print(buzz)


print('\nAll 5 year old cats')
# Select with query, all 5-year-old cats
age_5 = Cat.select().where(Cat.age == 5)
for cat in age_5:
    print(cat)

# Find one or none, useful when only one result is expected
holly_again = Cat.get_or_none(Cat.name == 'Holly')
print('\nCat called Holly:', holly_again)


# How many cats?
count = Cat.select().count()
print('\nThere are this many cats in the table:', count)

# Find one or none, useful when only one result is expected
molly = Cat.get_or_none(Cat.name == 'Molly')
print('\nCat called Molly:', molly)  # None


# Sorting
print('\nCats, sorted by name')
for cat in Cat.select().order_by(Cat.name):
    print(cat)

print('\nDeleting all cats')
# Delete all cats
Cat.delete().execute()

print('\nEverything in the database:')  # Nothing printed
for cat in Cat.select(Cat):
    print(cat)
