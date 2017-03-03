import sqlite3

cnn = sqlite3.connect('TSL.db')

cur = cnn.cursor()
print(cur.execute("select * from Books_Tab").fetchall())
#cur.execute("CREATE TABLE Books_Of_Snudent(ID INTEGER PRIMARY KEY AUTOINCREMENT, Student int NULL, Book int NULL, Date_Of_Receipt nvarchar(100) NULL, Date_Of_Return nvarchar(100) NULL)")
cnn.commit()

cnn.close()