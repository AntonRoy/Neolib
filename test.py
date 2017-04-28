import sqlite3
import executes_for_web

cnn = sqlite3.connect('TSL.db')
cur = cnn.cursor()

print(cur.execute("select * from Books_Tab WHERE Name_Of_Book = '{0}'".format('литература', 'коровина')).fetchall())
#print(cur.execute("select * from Main_Tab").fetchall())
#print(cur.execute("select * from Books_Of_Snudent").fetchall())
#cur.execute("DELETE FROM Books_Of_Snudent")
#cur.execute("delete from Books_Tab")
#cur.execute("delete from Main_Tab")
#cur.execute("delete from Books_Of_Snudent")
def update_seq(num):
    global cur
    cur.execute("update sqlite_sequence set seq = {0}".format(num))

#update_seq(0)



cnn.commit()
cnn.close()