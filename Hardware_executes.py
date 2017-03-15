import sqlite3
import vkplus
import settings
import datetime


vk = vkplus.VkPlus(settings.vk_login, settings.vk_password, settings.vk_app_id)


def fin_date():
    now = list(map(int, str(datetime.date.today()).split('-')))
    now[2] += 14
    if now[1] in (1, 3, 5, 7, 8, 10, 12):
        if now[2] > 31:
            now[1] += 1
            now[2] %= 31
    elif now[1] == 2:
        if now[2] > 28 and now[0] % 4 != 0:
            now[1] += 1
            now[2] %= 28
        elif now[2] > 29:
            now[1] += 1
            now[2] %= 29
    else:
        if now[2] > 30:
            now[1] += 1
            now[2] %= 30

    if now[1] > 12:
        now[1] %= 12
        now[0] += 1
    fin = list(map(str, now))
    if len(fin[1]) == 1:
        fin[1] = '0' + fin[1]
    return '-'.join(fin)


def registration(First_Name, Last_Name, ID_Vk, Sex, gym, grade):
    print('Trying to connect:')
    try:
        connection = sqlite3.connect('TSL.db', timeout=10)
        print('Connected')
    except:
        print('Could not connect')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Main_Tab (First_Name, Last_Name, ID_Vk, Sex, gym, Grade) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(First_Name, Last_Name, ID_Vk, Sex, gym, grade))
    connection.commit()
    connection.close()



def take_book(Student, Book):
    global vk
    print('Trying to connect:')
    try:
        connection = sqlite3.connect('TSL.db', timeout=10)
        print('Connected')
    except:
        print('Could not connect')
    cursor = connection.cursor()
    try:
        id_vk = cursor.execute("select ID_Vk from Main_Tab where ID = '{0}'".format(Student)).fetchall()[0][0]
    except:
        return False
    request = cursor.execute("select * from Books_Of_Snudent where Book = '{0}' and Student = '{1}'".format(Book, Student)).fetchall()
    if request and request[0]:
        vkplus.VkPlus.send(vk, user_id=id_vk, message='Вы уже брали эту книгу')
        return False
    cursor.execute(("INSERT INTO Books_Of_Snudent (Student, Book, Date_Of_Receipt, Date_Of_Return) VALUES ('{0}', '{1}', '{2}', '{3}')").format(Student, Book, str(datetime.date.today()), fin_date()))
    cursor.execute("update Books_Tab set In_Stock = In_Stock - 1 where ID = {0}".format(Book))
    connection.commit()
    vkplus.VkPlus.send(vk, user_id=id_vk, message='Вы успешно взяли книгу')
    connection.close()
    return True


def return_book(Student, Book):
    global vk
    print('Trying to connect:')
    try:
        connection = sqlite3.connect('TSL.db', timeout=10)
        print('Connected')
    except:
        print('Could not connect')
    cursor = connection.cursor()
    id_vk = cursor.execute("select ID_Vk from Main_Tab where ID = '{0}'".format(Student)).fetchall()[0][0]
    request = cursor.execute("select * from Books_Of_Snudent where Book = '{0}' and Student = '{1}'".format(Book, Student)).fetchall()
    print(id_vk)
    if not request or not request[0]:
        vkplus.VkPlus.send(vk, user_id=id_vk, message='Чтобы сдать книгу - её нужно сначала взять')
        return False
    cursor.execute(("DELETE FROM Books_Of_Snudent where Student = '{0}' and Book = '{1}'").format(Student, Book))
    connection.commit()
    cursor.execute("update Books_Tab set In_Stock = In_Stock + 1 where ID = {0}".format(Book))
    connection.commit()
    vkplus.VkPlus.send(vk, user_id=id_vk, message='Вы успешно сдали книгу')
    connection.close()
    return True


def login2id(login):
    print('Trying to connect:')
    try:
        connection = sqlite3.connect('TSL.db', timeout=10)
        print('Connected')
    except:
        print('Could not connect')
    cursor = connection.cursor()
    id = cursor.execute("select ID from Main_Tab where gym = '{0}'".format(login)).fetchall()[0][0]
    return id


def isbn2id(isbn):
    print('Trying to connect:')
    try:
        connection = sqlite3.connect('TSL.db', timeout=10)
        print('Connected')
    except:
        print('Could not connect')
    cursor = connection.cursor()
    id = cursor.execute("select ID from Books_Tab where ISBN = '{0}'".format(isbn)).fetchall()[0][0]
    return id