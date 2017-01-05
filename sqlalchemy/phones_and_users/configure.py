from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, Integer, String, Column
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship

## By default, SQLite doesn't enforce foreign keys.
# Have to tell SQLite to enforce them. You wouldn't need to do this for PostgreSQL or MySQL.
from sqlalchemy import event
from sqlalchemy.engine import Engine
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
## end SQLite specific code


Base = declarative_base()
engine = create_engine('sqlite:///user.db', echo=True)


class User(Base):

    # Define the table name
    __tablename__ = 'users'

    # And columns
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)   # Can limit string lengths, if desired. Can define other constraints, for example, prevent Null names

    phones = relationship("Phone", back_populates="user")  # Optional. Can use this so a User can have a list of associated Phone objects. sqlalchemy figures out what data to populate using the ForeignKey relationship.

    def __repr__(self):
        ''' why not __str__ ? __str__ is for user-friendly strings, __repr__ is for debugging info, should be to identify objects'''
        return 'User: id = {} name = {}'.format(self.id, self.name)


class Phone(Base):

    '''Defines metadata about a phones table. Will create Phone objects from rows in this table.
    Phone objects have a foreign key column for the user id of the user who has this phone '''

    # At the minimum, need a table name
    __tablename__ = 'phones'

    # And at least one column. id, brand, version, will be the column names, and the have the types specified.
    id = Column(Integer, primary_key=True)
    brand = Column(String, nullable=False)  # Prevent empty values
    version = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))  # The data is this column must be a value in the users table id column
    user = relationship("User", back_populates='phones')   # Optional but useful to get data from a the User object that this Phone has a relationship with, via the foreign key user_id


    def __repr__(self):
        '''Optional, return an unambiguous representation of this object, helpful for debugging'''
        return 'Phone: id = {} brand = {} version = {}, assigned to user = {}'.format(self.id, self.brand, self.version, self.user_id, self.user)


Base.metadata.create_all(engine)
