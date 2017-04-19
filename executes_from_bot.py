import sqlite3

def Book_In_Library(Name_Of_Book1, Author_Of_Book1):
    print('Trying to connect:')
    try:
        connection = sqlite3.connect('TSL.db')
        print('Connected')
    except:
        print('Could not connect')
    cursor = connection.cursor()
    request = cursor.execute(("select * from Books_Tab where Name_Of_Book like '%{0}%' and Author_Of_Book like '%{1}%' and Books_Tab.In_Stock > 0").format(Name_Of_Book1, Author_Of_Book1)).fetchall()
    connection.close()
    if request:
        return (True, request[0][3][0].upper() + request[0][3][1:], request[0][4].title())
    return False


def return_date():
    print('Trying to connect:')
    try:
        connection = sqlite3.connect('TSL.db')
        print('Connected')
    except:
        print('Could not connect')
    cursor = connection.cursor()
    data = cursor.execute("SELECT ID, Date_Of_Return from Books_Of_Snudent").fetchall()
    data1 = cursor.execute("SELECT ID_Vk from Main_Tab")
    data.extend(data1)
    return data



def Books_Of_Author_In_Library(Author):
    print('Trying to connect:')
    try:
        connection = sqlite3.connect('TSL.db')
        print('Connected')
    except:
        print('Could not connect')
    cursor = connection.cursor()
    request = cursor.execute("select Name_Of_Book, In_Stock from Books_Tab where Author_Of_Book like '%{0}%'".format(Author)).fetchall()
    connection.close()
    if request:
        return request
    return 'Извините, но книги данного автора не найдены'


def list_of_debts(ID_In_Database):
    print('Trying to connect:')
    try:
        connection = sqlite3.connect('TSL.db')
        print('Connected')
    except:
        print('Could not connect')
    cursor = connection.cursor()
    request = cursor.execute("select Book from Books_Of_Snudent where Student = '{0}'".format(ID_In_Database[0][0])).fetchall()
    print(request)
    debts = set()
    for debt in request:
        debtf = cursor.execute("select * from Books_Tab where ID = '{0}'".format(debt[0])).fetchall()
        debts.add(debtf[0])
    print(list(debts))
    return list(debts)
    connection.close()


def ID_Of_Name(ID_Vk):
    print('Trying to connect:')
    try:
        connection = sqlite3.connect('TSL.db')
        print('Connected')
    except:
        print('Could not connect')
    cursor = connection.cursor()
    request = cursor.execute("select ID from Main_Tab where ID_Vk = '{0}'".format(ID_Vk)).fetchall()
    connection.close()
    return request


def Book_Of_Id(ID):
    print('Trying to connect:')
    try:
        connection = sqlite3.connect('TSL.db')
        print('Connected')
    except:
        print('Could not connect')
    cursor = connection.cursor()
    request = cursor.execute("select Name_Of_Book, Author_Of_Book from Main_Books_Tab where ID = '{0}'".format(ID)).fetchall()
    connection.close()
    return request


def Books_Of_Genre_In_Library(Genre):
    print('Trying to connect:')
    try:
        connection = sqlite3.connect('TSL.db')
        print('Connected')
    except:
        print('Could not connect')
    cursor = connection.cursor()
    request = cursor.execute("select Name_Of_Book, Author_Of_Book, In_Stock from Books_Tab where Genre like '%{0}%'".format(Genre)).fetchall()
    connection.close()
    if request:
        return request
    return 'Извините, но книги данного жанра не найдены'