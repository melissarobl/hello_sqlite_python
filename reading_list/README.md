## Bookstore with sqlite

###New features

* SQLlite generates a rowid column, which is an autoincrementing integer. Note that in queries, you have to explicitly select it. 
* Wrapping and rethrowing exceptions with the `raise BookException('oops') from e` syntax, if `e` is another exception.
* The `lastrowid` attribute of cursors, for knowing what the rowid of a new row is after an insert, 
* The `rowcount` attribute of cursors, for counting the number of rows affected after a delete or update.  

###Running the unittests

`python -m unittest discover test`