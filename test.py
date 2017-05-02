import sqlite3

cnn = sqlite3.connect('TSL.db')
cur = cnn.cursor()

from executes_for_web import *

#print(stud2arch('1234'))

cur.execute("DELETE FROM Books_Tab WHERE ID = 4")


cnn.commit()
cnn.close()