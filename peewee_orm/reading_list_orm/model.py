from peewee import *
from database_config import database_path


db = SqliteDatabase(database_path)


class Book(Model):

    """ Represents a book in the database """

    # TODO add the constraint that title + author should be unique

    title = CharField()
    author = CharField()
    read = BooleanField(default=False)


    class Meta:
        database = db
        indexes = (
            (('title', 'author'), True),
        )

    def __str__(self):
        read_status = 'have' if self.read else 'have not'
        return f'ID {self.id}, Title: {self.title}, Author: {self.author}. You {read_status} read this book.'


db.connect()
db.create_tables([Book])
