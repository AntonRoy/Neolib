import sqlite3

cnn = sqlite3.connect('TSL.db')
cur = cnn.cursor()
print(cur.execute("select * from Books_Tab").fetchall())
print(cur.execute("select * from Main_Tab").fetchall())
#cur.execute("DELETE FROM Books_Tab where ID = 5")
#cur.execute("update sqlite_sequence set seq = 4")
cnn.commit()
cnn.close()