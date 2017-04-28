import sqlite3
from bs4 import BeautifulSoup
import urllib.request
from correct import correct

def reduce(lis):
    i = 2
    a = lis[0] & lis[1]
    while i < len(lis):
        ok = False
        for j in range(i, len(lis)):
            if len(lis[j]):
                i = j
                ok = True
                break
        if not ok:
            break
        a = a & lis[i]
        i += 1
    return a


def getSmeta(ID):
    print('Trying to connect:')
    try:
        connection = sqlite3.connect('TSL.db', timeout=10)
        print('Connected')
    except:
        print('Could not connect')
    cursor = connection.cursor()
    data = cursor.execute("SELECT * FROM Main_Tab WHERE gym = '{0}'".format(ID)).fetchall()
    return data


def update_data(gym, name, surename, sex, grade, id_vk):
    print('Trying to connect:')
    try:
        connection = sqlite3.connect('TSL.db', timeout=10)
        print('Connected')
    except:
        print('Could not connect')
    cursor = connection.cursor()
    cursor.execute("update Main_Tab SET First_Name = '{1}' WHERE gym = '{0}'".format(gym, name))
    cursor.execute("update Main_Tab SET Last_Name = '{1}' WHERE gym = '{0}'".format(gym, surename))
    cursor.execute("update Main_Tab SET Sex = '{1}' WHERE gym = '{0}'".format(gym, sex))
    cursor.execute("update Main_Tab SET grade = '{1}' WHERE gym = '{0}'".format(gym, grade))
    cursor.execute("update Main_Tab SET id_vk = '{1}' WHERE gym = '{0}'".format(gym, id_vk))
    connection.commit()
    connection.close()
    return True


def update_BookData(old_name, old_auth, name, author):
    print('Trying to connect:')
    try:
        connection = sqlite3.connect('TSL.db', timeout=10)
        print('Connected')
    except:
        print('Could not connect')
    cursor = connection.cursor()
    cursor.execute("update Books_Tab SET Name_Of_Book = '{2}' WHERE Name_Of_Book = '{0}' and Author_Of_Book = '{1}'".format(old_name, old_auth, name.lower()))
    cursor.execute("update Books_Tab SET Author_Of_Book = '{2}' WHERE Name_Of_Book = '{0}' and Author_Of_Book = '{1}'".format(old_name, old_auth, author.lower()))
    connection.commit()
    connection.close()
    return True


def mega_search(**kwargs):
    print('Trying to connect:')
    try:
        connection = sqlite3.connect('TSL.db', timeout=10)
        print('Connected')
    except:
        print('Could not connect')
    cursor = connection.cursor()
    sets = []
    if len(kwargs.items()) == 1:
        arg = list(kwargs.items())[0]
        return list(map(list, list([cursor.execute(("select First_Name, Last_Name from Main_Tab where {0} LIKE '%{1}%'").format(arg[0], arg[1])).fetchall()])))
    for arg in kwargs.items():
        if arg[1] == '':
            continue
        sets.append(set(cursor.execute(("select First_Name, Last_Name from Main_Tab where {0} LIKE '%{1}%'").format(arg[0], arg[1])).fetchall()))
    sets = sets if len(sets) <= 1 else [reduce(sets)]
    return list(map(list, list(sets)))


def mega_searchBook(**kwargs):
    print('Trying to connect:')
    try:
        connection = sqlite3.connect('TSL.db', timeout=10)
        print('Connected')
    except:
        print('Could not connect')
    cursor = connection.cursor()
    sets = []
    if len(kwargs.items()) == 1:
        arg = list(kwargs.items())[0]
        return list(map(list, list([cursor.execute(("select Name_Of_Book, Author_Of_Book from Books_Tab where {0} LIKE '%{1}%'").format(arg[0], arg[1])).fetchall()])))
    for arg in kwargs.items():
        if arg[1] == '':
            continue
        sets.append(set(cursor.execute(("select Name_Of_Book, Author_Of_Book from Books_Tab where {0} LIKE '%{1}%'").format(arg[0], arg[1])).fetchall()))
    sets = sets if len(sets) <= 1 else [reduce(sets)]
    return list(map(list, list(sets)))


def add_book_f(Name, Auth, isbn, cnt):
    print('Trying to connect:')
    try:
        connection = sqlite3.connect('TSL.db', timeout=10)
        print('Connected')
    except:
        print('Could not connect')
    cursor = connection.cursor()
    cursor.execute(("INSERT INTO Books_Tab (ISBN, Name_Of_Book, Author_Of_Book, In_Stock, All_Books) VALUES ('{0}', '{1}', '{2}', '{3}', '{3}')").format(isbn, Name.lower(), Auth.lower(), cnt))
    connection.commit()
    connection.close()
    return [True, Name, Auth]


def Add_Book(isbn, cnt):
    print('Trying to connect:')
    try:
        connection = sqlite3.connect('TSL.db', timeout=10)
        print('Connected')
    except:
        print('Could not connect')
    cursor = connection.cursor()
    request1 = cursor.execute(("select * from Books_Tab where ISBN = '{0}'").format(isbn)).fetchall()
    if request1:
        cursor.execute(("update Books_Tab set In_Stock = In_Stock + {1} where ISBN = '{0}'").format(isbn, cnt))
        cursor.execute(("update Books_Tab set All_Books = All_Books + {1} where ISBN = '{0}'").format(isbn, cnt))
        name = request1[0][3]
        auth = request1[0][4]
        connection.commit()
        connection.close()
        return (True, name, auth)
    book_meta = list(heh(isbn))
    try:
        book_meta[1] = correct(book_meta[1])
    except:
        pass
    try:
        book_meta[2] = correct(book_meta[2])
    except:
        pass
    if not book_meta[0]:
        connection.commit()
        connection.close()
        return (False, False, False)
    request2 = cursor.execute("INSERT INTO Books_Tab "
                               "(ISBN, Name_Of_Book, Author_Of_Book, In_Stock, All_Books) "
                               "VALUES "
                               "('{0}', '{1}', '{2}', '{3}', '{3}')".format(isbn,
                                                                            book_meta[1].lower(),
                                                                            book_meta[2].lower(),
                                                                            cnt)).fetchall()
    connection.commit()
    connection.close()
    return book_meta


def Search_Of_Student(name):
    print('Trying to connect:')
    try:
        connection = sqlite3.connect('TSL.db', timeout=10)
        print('Connected')
    except:
        print('Could not connect')
    id = ID_Of_Name((name[0], name[1]))
    cursor = connection.cursor()
    request = cursor.execute(("SELECT Book, Date_Of_Receipt, Date_Of_Return FROM Books_Of_Snudent WHERE Student = '{0}'").format(id)).fetchall()
    request = list(map(lambda x: list(x), request))
    for book in range(len(request)):
        book_name = cursor.execute(("SELECT Name_Of_Book FROM Books_Tab WHERE ID = '{0}'").format(request[book][0])).fetchall()
        request[book][0] = book_name[0][0]
    connection.close()
    return request


def Search_Of_Book(Book, Author):
    print('Trying to connect:')
    try:
        connection = sqlite3.connect('TSL.db', timeout=10)
        print('Connected')
    except:
        print('Could not connect')
    cursor = connection.cursor()
    id = ID_Of_Book(Book, Author)
    request = cursor.execute(("select Student, Date_Of_Receipt, Date_Of_Return FROM Books_Of_Snudent WHERE Book = '{0}'").format(id)).fetchall()
    request = list(map(lambda x: list(x), request))
    for student in range(len(request)):
        student_name = cursor.execute(("SELECT First_Name, Last_Name FROM Main_Tab WHERE ID = '{0}'").format(request[student][0])).fetchall()
        request[student][0] = student_name[0][0] + ' ' + student_name[0][1]
    connection.close()
    return request


def select_tab(tab, start_line):
    print('Trying to connect:')
    try:
        connection = sqlite3.connect('TSL.db', timeout=10)
        print('Connected')
    except:
        print('Could not connect')
    cursor = connection.cursor()
    if tab:
        return list(map(lambda x: x[:-1], cursor.execute("select * from Books_Tab WHERE ID >= '{0}' and ID < '{0}' + 10".format(start_line)).fetchall()))
    return list(map(lambda x: x[:-2], cursor.execute("select * from Main_Tab WHERE ID >= '{0}' and ID < '{0}' + 10".format(start_line)).fetchall()))
    connection.close()


def ID_Of_Name(name):
    print('Trying to connect:')
    try:
        connection = sqlite3.connect('TSL.db', timeout=10)
        print('Connected')
    except:
        print('Could not connect')
    cursor = connection.cursor()
    name = list(name)
    name[0] = name[0].lower().title()
    name[1] = name[1].lower().title()
    request = cursor.execute(("select ID from Main_Tab where First_Name LIKE '%{0}%' and Last_Name LIKE '%{1}%'").format(name[0], name[1])).fetchall()
    connection.close()
    return request[0][0]


def ID_Of_Book(Name, Author):
    print('Trying to connect:')
    try:
        connection = sqlite3.connect('TSL.db', timeout=10)
        print('Connected')
    except:
        print('Could not connect')
    cursor = connection.cursor()
    Name = Name.lower()
    Author = Author.lower()
    request = cursor.execute(("select ID from Books_Tab where Name_Of_Book LIKE '%{0}%' and Author_Of_Book LIKE '%{1}%'").format(Name, Author)).fetchall()
    connection.close()
    return request[0][0]


def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()


def heh(isb):
    html = get_html('http://www.bookfinder.com/search/?author=&title=&lang=en&isbn='+ str(isb) + '&new_used=*&destination=ru&currency=RUB&mode=basic&st=sr&ac=qr')
    soup = BeautifulSoup(html)
    book_name = soup.find('span', itemprop='name')
    book_author = soup.find('span', itemprop='author')
    lang = str(soup.find('span', itemprop='inLanguage', class_="describe-isbn"))
    lang = lang[lang.find('>') + 1:lang.find('</')]
    try:
        book_name = str(book_name.prettify())
        book_name = book_name[book_name.find('>') + 1:book_name.find('</') - 1]
        book_author = str(book_author.prettify())
        book_author = book_author[book_author.find('>') + 1:book_author.find('>/') - 6]
        return (True, translit(book_name[2:], lang), author(translit(book_author[2:-1], lang)))
    except:
        return (False, None)


def translit(s, lang):
    if 'russian' not in lang.lower():
        return s
    i = 0
    s = s.lower()
    sf = ''
    dict = {'a': 'а', 'b': 'б', 'v': 'в', 'g': 'г', 'd': 'д', 'e': 'е', 'z': 'з', 'i': 'и', 'y': 'ы', 'k': 'к',
            'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о', 'p': 'п', 'r': 'р', 's': 'с', 't': 'т', 'u': 'у', 'f': 'ф',
            'c': 'ц', 'h':'х'}
    while i < len(s) - 1:
        if s[i] == 'j':
            i += 1
            if s[i] == 'e':
                sf += 'ё'
            elif s[i] == 's':
                i += 1
                if s[i] == 'h':
                    sf += 'щ'
            elif s[i] == 'u':
                sf += 'ю'
            elif s[i] == 'h':
                sf += 'ь'
            elif s[i] == 'a':
                sf += 'я'
        elif s[i] == 'z' and s[i + 1] == 'h':
            i += 1
            sf += 'ж'
        elif s[i] == 'k' and s[i + 1] == 'h':
            i += 1
            sf += 'х'
        elif s[i] == 'c' and s[i + 1] == 'h':
            i += 1
            sf += 'ч'
        elif s[i] == 's' and s[i + 1] == 'h':
            i += 1
            sf += 'ш'
        elif s[i] == 'h' and s[i + 1] == 'h':
            i += 1
            sf += 'ъ'
        elif s[i] == 'i' and s[i + 1] == 'h':
            i += 1
            sf += 'ы'
        elif s[i] == 'e' and s[i + 1] == 'h':
            i += 1
            sf += 'э'
        else:
            if s[i] not in dict.keys():
                sf += s[i]
            else:
                sf += dict[s[i]]
        i += 1
    if len(s) != len(sf):
        if s[-1] not in dict.keys():
            sf += s[-1]
        else:
            sf += dict[s[-1]]
    s = list(sf)
    delit = False
    for i in range(len(s) - 1):
        if (s[i] == 'и' or s[i] == 'й') and s[i + 1] == 'а':
            s[i] = 'я'
            s[i + 1] = ''
        elif s[i] == 'и' and s[i + 1] == 'и':
            s[i+1] = 'й'
        elif s[i] == 'й' and s[i + 1] == 'у':
            s[i] = 'ю'
            s[i + 1] = ''
        elif s[i] == 'ы' and s[i + 1] == 'a':
            s [i] = ''
        elif s[i] == 'т' and s[i + 1] == 'ц':
            s[i] = ''
        elif s[i] == 'ы' and s[i + 1] == 'а':
            s[i] = 'я'
            s[i + 1] = ''
        elif s[i] == 'с' and s[i + 1] == 'ч':
            s[i] = 'щ'
            s[i + 1] = ''
        elif s[i] == 'т' and s[i + 1] == 'с':
            s[i] = 'ц'
            s[i + 1] = ''
        elif s[i] == 'е' and s[i + 1] == 'и':
            s[i + 1] = 'й'
        elif s[i] == 'и' and s[i + 1] == 'ы':
            s[i + 1] = 'й'
        elif s[i] == 'ш' and s[i + 1] == 'ч':
            s[i] = 'щ'
            s[i + 1] = ''
        elif s[i] == 'ы' and s[i + 1] == 'у':
            s[i] = 'ю'
            s[i + 1] = ''
        elif s[i] == 'х' and s[i] == s[i + 1]:
            s[i] = ''
        elif s[i] == '.':
            s[i] = ''
        if s[i] == '[':
            delit = True
        if delit:
            s[i] = ''
        if s[i] == ']':
            delit = False
        if s[i] in set(list(',.;')):
            s[i] = ''
        elif s[i] in set(list('abcdefghijklmnopqrstuvwxyz')):
            s[i] = ''
    if s[-1] in set(list('-,.;')):
        s[-1] = ''
    if s[-1] in set(list('abcdefghijklmnopqrstuvwxyz')):
        s[-1] = ''
    s = list(''.join(s))
    if s[-2] == ' ' and s[-1] not in set(list('скуова')):
        s[-2] = ''
        s[-1] = ''
    s[0] = s[0].upper()
    return ''.join(s)


def author(auth):
    auth = auth.split()
    auth = list(map(lambda x: x[0].upper() + x[1:], auth))
    auth = list(map(lambda x: x[0] if len(x) == 2 else x, auth))
    return ' '.join(auth)