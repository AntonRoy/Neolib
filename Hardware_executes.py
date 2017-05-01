import sqlite3
import vkplus
import settings
import datetime
import vk_api


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
    try:
        connection = sqlite3.connect('TSL.db', timeout=10)
    except:
        print('Could not connect')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Main_Tab (ID, First_Name, Last_Name, ID_Vk, Sex, gym, Grade) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')".format(cursor.execute("SELECT COUNT(*) FROM Main_Tab").fetchall()[0][0] + 1, First_Name, Last_Name, ID_Vk, Sex, gym, grade))
    connection.commit()
    connection.close()


def getIdByURL(url):
    url = url.split('/')[-1]
    boom = vk_api.VkApi()
    result = boom.method('users.get', {'user_ids':url})
    return result[0]['id']


def take_book(Student, Book):
    global vk
    try:
        connection = sqlite3.connect('TSL.db', timeout=10)
    except:
        print('Could not connect')
    cursor = connection.cursor()
    Student = login2id(Student)
    Book = isbn2id(Book)
    if not Book:
        return (False, 'Этой книги нет в библиотеке')
    try:
        id_vk = cursor.execute("select ID_Vk from Main_Tab where ID = '{0}'".format(Student)).fetchall()[0][0]
        if not id_vk:
            print(1//0)
    except:
        request = cursor.execute("select * from Books_Of_Snudent where Book = '{0}' and Student = '{1}'".format(Book, Student)).fetchall()
        if request and request[0]:
            return (False, 'Вы уже брали эту книгу')
        cursor.execute(("INSERT INTO Books_Of_Snudent (Student, Book, Date_Of_Receipt, Date_Of_Return) VALUES ('{0}', '{1}', '{2}', '{3}')").format(Student, Book, str(datetime.date.today()), fin_date()))
        cursor.execute("update Books_Tab set In_Stock = In_Stock - 1 where ID = {0}".format(Book))
        connection.commit()
        connection.close()
        return (True)
    request = cursor.execute("select * from Books_Of_Snudent where Book = '{0}' and Student = '{1}'".format(Book, Student)).fetchall()
    if request and request[0]:
        try:
            vkplus.VkPlus.send(vk, user_id=id_vk, message='Вы уже брали эту книгу')
        except:
            vkplus.VkPlus.addUser(vk, id_vk)
        return (False, 'Вы уже брали эту книгу')
    cursor.execute(("INSERT INTO Books_Of_Snudent (Student, Book, Date_Of_Receipt, Date_Of_Return) VALUES ('{0}', '{1}', '{2}', '{3}')").format(Student, Book, str(datetime.date.today()), fin_date()))
    cursor.execute("update Books_Tab set In_Stock = In_Stock - 1 where ID = {0}".format(Book))
    connection.commit()
    try:
        vkplus.VkPlus.send(vk, user_id=id_vk, message='Вы успешно взяли книгу')
    except:
        pass
    connection.close()
    return (True)


def return_book(Student, Book):
    global vk
    try:
        connection = sqlite3.connect('TSL.db', timeout=10)
    except:
        print('Could not connect')
    cursor = connection.cursor()
    Student = login2id(Student)
    Book = isbn2id(Book)
    if not Book:
        return (False, 'Этой книги нет в библиотеке')
    try:
        id_vk = cursor.execute("select ID_Vk from Main_Tab where ID = '{0}'".format(Student)).fetchall()[0][0]
        if not id_vk:
            print(1//0)
    except:
        request = cursor.execute(
            "select * from Books_Of_Snudent where Book = '{0}' and Student = '{1}'".format(Book, Student)).fetchall()
        if not request:
            return (False, 'Чтобы сдать книгу - её нужно сначала взять')
        cursor.execute(("DELETE FROM Books_Of_Snudent where Student = '{0}' and Book = '{1}'").format(Student, Book))
        connection.commit()
        cursor.execute("update Books_Tab set In_Stock = In_Stock + 1 where ID = {0}".format(Book))
        connection.commit()
        return (True)
    request = cursor.execute("select * from Books_Of_Snudent where Book = '{0}' and Student = '{1}'".format(Book, Student)).fetchall()
    if not request or not request[0]:
        vkplus.VkPlus.send(vk, user_id=id_vk, message='Чтобы сдать книгу - её нужно сначала взять')
        return (False, 'Чтобы сдать книгу - её нужно сначала взять')
    cursor.execute(("DELETE FROM Books_Of_Snudent where Student = '{0}' and Book = '{1}'").format(Student, Book))
    connection.commit()
    cursor.execute("update Books_Tab set In_Stock = In_Stock + 1 where ID = {0}".format(Book))
    connection.commit()
    try:
        vkplus.VkPlus.send(vk, user_id=id_vk, message='Вы успешно сдали книгу')
    except:
        pass
    connection.close()
    return (True)


def true_code(code):
    try:
        connection = sqlite3.connect('TSL.db', timeout=10)
    except:
        print('Could not connect')
    cursor = connection.cursor()
    return cursor.execute("select * from Main_Tab where gym == '{0}'".format(code)).fetchall()


def login2id(login):
    try:
        connection = sqlite3.connect('TSL.db', timeout=10)
    except:
        print('Could not connect')
    cursor = connection.cursor()
    print('login: ', login)
    id = cursor.execute("select ID from Main_Tab where gym = '{0}'".format(login)).fetchall()[0][0]
    return id


def isbn2id(isbn):
    try:
        connection = sqlite3.connect('TSL.db', timeout=10)
    except:
        print('Could not connect')
    cursor = connection.cursor()
    try:
        id = cursor.execute("select ID from Books_Tab where ISBN = '{0}'".format(isbn)).fetchall()[0][0]
    except:
        return False
    return id