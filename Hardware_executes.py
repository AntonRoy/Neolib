import sqlite3
import vkplus
import settings

vk = vkplus.VkPlus(settings.vk_login, settings.vk_password, settings.vk_app_id)

#def registration(First_Name, Last_Name, ID_Vk, gym, )


def take_book(Student, Book):
    global vk
    print('Trying to connect:')
    try:
        connection = sqlite3.connect('TSL.db', timeout=10)
        print('Connected')
    except:
        print('Could not connect')
    cursor = connection.cursor()
    request = cursor.execute(("INSERT INTO Books_Of_Snudent (Student, Book) VALUES ('{0}', '{1}')").format(Student, Book))
    cursor.execute("update Books_Tab set In_Stock = In_Stock - 1 where ID = {0}".format(Book))
    id_vk = cursor.execute("select ID_Vk from Main_Tab where ID = '{0}'".format(Student))
    connection.commit()
    vkplus.VkPlus.send(vk, user_id=id_vk, message='Вы успешно взяли книгу')
    connection.close()
    return


def return_book(Student, Book):
    global vk
    print('Trying to connect:')
    try:
        connection = sqlite3.connect('TSL.db', timeout=10)
        print('Connected')
    except:
        print('Could not connect')
    cursor = connection.cursor()
    request = cursor.execute(("DELETE FROM Books_Of_Snudent where Student = '{0}' and Book = '{1}'").format(Student, Book))
    cursor.execute("update Books_Tab set In_Stock = In_Stock + 1 where ID = {0}".format(Book))
    id_vk = cursor.execute("select ID_Vk from Main_Tab where ID = '{0}'".format(Student))
    connection.commit()
    vkplus.VkPlus.send(vk, user_id=id_vk, message='Вы успешно сдали книгу')
    connection.close()
    return


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