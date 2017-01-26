from sqlalchemy import Column, Integer, String

from sqlalchemy.ext.declarative import declarative_base # From docs: 'Classes mapped using the Declarative
# system are defined in terms of a base class which maintains a catalog of classes and tables relative to that base -
# this is known as the declarative base class.'

from base import Base

class Phone(Base):

    '''Defines metadata about a phones table. Will create Phone objects from rows in this table. '''

    # At the minimum, need a table name
    __tablename__ = 'phones'

    # And at least one column. id, brand, version, will be the column names, and the have the types specified.
    id = Column(Integer, primary_key=True)
    brand = Column(String)
    version = Column(Integer)

    def __repr__(self):
        '''Optional, return an unambiguous representation of this object, helpful for debugging'''
        return 'Phone: id = {} brand = {} version = {}'.format(self.id, self.brand, self.version)
