from peewee import *
import peewee_validates
from peewee_validates import ModelValidator
from peewee_validates import validate_not_empty, validate_required, validate_length, validate_range
from config import database_path

db = SqliteDatabase(database_path)

# Name may not be empty
# Country must be at least 2 characters and not more than 100 
# Catches must be at least 1 and not more than 1000

# Note if you modify a table column, you need to drop your database table and recreate 
# The easiest way may be to delete the database file

class ChainsawRecord(Model):
    name = CharField(null=False, unique=True, constraints=[Check('length(name) >= 1')])
    country = CharField(null=False, constraints=[Check('length(country) >= 2')])
    catches = IntegerField(null=False, constraints=[Check('catches >= 1'), Check('catches <= 1000')])

    class Meta:
        database = db

    def __str__(self):
        return f'{self.id or "No ID"}: {self.name}, {self.country}, catches: {self.catches}'


db.create_tables([ChainsawRecord])