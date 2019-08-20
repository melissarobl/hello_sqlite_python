from peewee import *
from database_config import database_path

db = SqliteDatabase(database_path)

class Book(Model):

    """ Represents a book in the database """

    title = CharField()
    author = CharField()
    read = BooleanField(default=False)


    class Meta:
        database = db
        constraints = [SQL('UNIQUE( title COLLATE NOCASE, author COLLATE NOCASE )')]


    def __str__(self):
        read_status = 'have' if self.read else 'have not'
        return f'ID {self.id}, Title: {self.title}, Author: {self.author}. You {read_status} read this book.'


db.connect()
db.create_tables([Book])
