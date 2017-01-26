from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# Engine represents the core interface to the database
# The first argument is the url of the database; this points to a sqlitedb saved in a file called phone.db
engine = create_engine('sqlite:///phone.db', echo=True)   # Create engine. echo=True turns on logging
Base = declarative_base()  # All of the mapped classes inherit from this class.
# Need one instance that everything shares.
