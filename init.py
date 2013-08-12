# initialize the database
import sqlite3

conn = sqlite3.connect('bookmarks.db')

c = conn.cursor()

c.execute('''
CREATE TABLE records
(ID TEXT, TIME TEXT, LINK TEXT, TITLE TEXT, 
DESC TEXT, TAG TEXT, READ INTEGER, NOTES TEXT)
''')

conn.commit()

c.close()
