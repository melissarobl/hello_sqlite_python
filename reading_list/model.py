from dataclasses import dataclass, field

# TODO add a docstring for this module.

NO_ID = -1


@dataclass
class Book:

    # TODO add a docstring for this class to explain it's purpose

    title: str
    author: str
    read: bool = False
    id: int = NO_ID

    def __str__(self):
        read_status = 'have' if self.read else 'have not'
        return f'ID {self.id}, Title: {self.title}, Author: {self.author}. You {read_status} read this book.'
