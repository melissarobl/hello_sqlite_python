from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from base import Base

# # Engine represents the core interface to the database
# # The first argument is the url of the database; this points to a sqlitedb saved in a file called phone.db
engine = create_engine('sqlite:///phone.db', echo=False)   # Create engine. echo=True turns on logging
#
from phone import Phone
#
# # Base = declarative_base()  # All of the mapped classes inherit from this class.
# #
Base.metadata.create_all(engine) # Create a table for all the things that use Base

#Create a phone object. Use named args to set the values of the object
phone = Phone(brand='Samsung', version=6)
# can also read and set variables of the phone object
phone.version=7
print(phone.brand)
print(phone)    # Calls __repr__

# The phone is not saved to the database yet.

# Need a Session to talk to the database. This is what manages connections to the DB.
# And, the session manages objects that are mapped to rows in the database.

#Make a Session class... Only need to do this one time.
Session = sessionmaker(bind=engine)   #Use the engine created earlier

# Ask the Session to instantiate a session object. We'll use the session object to talk to the DB
save_session = Session()

save_session.add(phone)   # The phone is pending - not yet saved. It won't be until the session is committed, or closed

save_session.commit()  # now phone should be saved

# Can add more phones

phone2 = Phone(brand='iPhone', version=6)
phone3 = Phone(brand='Nokia', version=3)
phone4 = Phone(brand='Motorola', version=4)

save_session.add_all([ phone2, phone3, phone4 ])

print(save_session.new)   # The newly added phones
print(save_session.dirty)   # empty set

save_session.commit()   # All data saved. Now nothing is new, or dirty

phone4.version = 10   # The session tracks the objects that are added to it
# So if you change any of the data in any of the tracked objects, it will be added as a pending change in the DB

print(save_session.new)  # Empty set
print(save_session.dirty)   #Anything that's been changed since the last commit

save_session.commit()  # Will update the record for phone4

save_session.close()

## Querying

search_session = Session()

# Fetch everything.
# Query returns Phone objects
for phone in search_session.query(Phone):
    print(phone)

# Fetch first phone, get a Phone object
print(search_session.query(Phone).first())

# Expect exactly one result? use one() which will return an object; or an error if there are 0 or 2+ items
print(search_session.query(Phone).filter_by(id=4).one())  # Useful for primary keys, will expect exactly one result

# Query that return 0 rows - difference between first() and one()
print(search_session.query(Phone).filter_by(id=4000).first())   # None

try:
    print(search_session.query(Phone).filter_by(id=4000).one())   # Error
except:
    print('calling one() when there are 0 or 2+ results causes an error')

print('One or none')
#Or, can use one_or_none. Returns None, or the first matching object, if found.
print(search_session.query(Phone).filter_by(id=4).one_or_none())   # Phone 3 data
print(search_session.query(Phone).filter_by(id=4000).one_or_none())   # None


# If you want a list to use in the program, not a iterator, use the all() method

results = search_session.query(Phone).all() # A list of all phone objects
print(results)

results = search_session.query(Phone).filter(Phone.version > 4).all()

print(type(results))    # A list
print(type(search_session.query(Phone)))  # A query object - you can loop over this if needed, or call all() or first() or one()


# Fetch first phone, get a Phone object
print(search_session.query(Phone).first())


# Fetch only named columns as a tuple
for brand, version in search_session.query(Phone.brand, Phone.version):
    print(brand, version)

# Order by
for phone in search_session.query(Phone).order_by(Phone.brand):
    print(phone)


# filter_by - basic where clause to match items

# Match rows where brand = 'Nokia'
for phone in search_session.query(Phone).filter_by(brand='Nokia'):
    print(phone)

# Match rows where branc = 'Nokia' and version = 3
for phone in search_session.query(Phone).filter_by(brand='Nokia', version=3):
    print(phone)

# Filter, can use < > != == operators
# Notice you need to use Class.field == instead of
# Match phones where version is not 4
for phone in search_session.query(Phone).filter(Phone.version != 4):
    print(phone)

# Matching with like, call a function. Match all phones with 'o' in the brand
for phone in search_session.query(Phone).filter(Phone.brand.like('%s%')):
    print(phone)

# Match phones where version is greater than 4
for phone in search_session.query(Phone).filter(Phone.version > 4):
    print(phone)

# Match phones where version is less than or equal to 4
for phone in search_session.query(Phone).filter(Phone.version <= 4):
    print(phone)

# Can chain methods
# Match phones where version is greater than 4, order by brand
for phone in search_session.query(Phone).filter(Phone.version > 4).order_by(Phone.brand):
    print(phone)

# Count the rows returned with count(). How many phones with version greater than 4?
print( search_session.query(Phone).filter(Phone.version > 4).count() )

search_session.close()   # Done with session. Close.
# Once the session is closed, the objects added are detatched and you won't be able to query their state.


## Updating the DB - query, find an object, update it, save
update_session = Session()

# Do a query. old_phones is a list of phones
old_phones = update_session.query(Phone).filter(Phone.version < 4)

# update phones in old_phones. Add one to version number
for phone in old_phones:
    phone.version += 1    # Because the phones are tracked by SQLAlchemy, it will know about these changes

update_session.commit()  # So they'll be saved when you commit

update_session.close()
# Or can modify objects that have been created in code and added to a session, as above.


## Delete

delete_session = Session()

# Delete the phone3 object. It doesn't have to be a object tracked by the session that it was added to.
delete_session.delete(phone3)
delete_session.commit()  # And commit

# Query, and delete
for phone in delete_session.query(Phone).filter_by(brand='iPhone'):
    delete_session.delete(phone)
delete_session.commit()
