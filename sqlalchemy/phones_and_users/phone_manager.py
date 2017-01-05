import configure   # Runs the code in the configure module to set up the mappings
from configure import User, Phone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///user.db', echo=False)

Session = sessionmaker(bind=engine)

print('Welcome to the phone manager')

# Create some users

alice = User(name='Alice')
bob = User(name='Bob')

new_user_name = input('Enter name for a new user: ')

new_user = User(name=new_user_name)

save_users = Session()
save_users.add_all( [ alice, bob, new_user ] )
save_users.commit()
save_users.close()

print()

# And some phones

samsung = Phone(brand='Samsung', version=7)
apple = Phone(brand='iPhone', version=6)

new_phone_brand = input('Enter a phone brand: ')
new_phone_version = int(input('Enter version number (as an integer): '))  # todo here, and other places - validate int input
new_phone = Phone(brand=new_phone_brand, version=new_phone_version)

save_phones = Session()
save_phones.add_all( [ samsung, apple, new_phone ] )
save_phones.commit()
save_phones.close()

print()

# Assign the phones to users. One user can have zero or any number of phones.

assign_session = Session()

print('Here are all the users')

for user in assign_session.query(User):
    print(user)

print()

print('Here are all the phones:')
for phone in assign_session.query(Phone):
    print(phone)

print()

# Assign phones to users. You might want to assign more than one phone to a particular user
# When you create your DB design, you'll think about whether your foreign key relationships
# are one-to-one, many-to-many, one-to-many; and specify that in your schema.
print('Please assign a phone to each user. You can assign more than one phone to any user. ')

for phone in assign_session.query(Phone):
    print('Who should this phone be assigned to? ' + str(phone))
    user_id = int(input('Enter user id: '))

    try:
        phone.user_id = user_id
        assign_session.commit()  # Will error at commit if user id does not exists - violates foreign key constraint.
        print('Assigned phone to user {}'.format(phone.user) )  # The phone.user field automatically gets populated with the user data. Neat! 

    except:
        assign_session.rollback()  # Have to roll back the attempt to set the phone user id to invalid values
        phone.user_id = None    # Remove the invalid data
        print('Error: no user with id {}. No changes made to DB'.format(user_id))   # todo have user try again

assign_session.commit()

print()

print('Here are the phones with their assigned users:')
for phone in assign_session.query(Phone):
    print(phone)
    # Can also get the user with phone.user

print()

print('Here are all the users')
for user in assign_session.query(User):
    print(user)
    if len(user.phones) > 0:
        print(user.phones)
    else :
        print('User has no phones assigned')


assign_session.close()
