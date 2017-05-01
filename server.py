from flask import *
from flask_bootstrap import Bootstrap
import os
import executes_for_web
#import Hardware_executes

app = Flask(__name__)
bootstrap = Bootstrap(app)

username = 'a1'
password = 'a1'


@app.route('/')
def start():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return redirect(url_for('main'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':

        if request.form['login'] == username and request.form['password'] == password:
            session['logged_in'] = True
            return redirect(url_for('main'))
        else:
            error = " Неверный логин/пароль"
    return render_template('about.html', error=error, result='')


@app.route('/main', methods=['GET', 'POST'])
def main():
    stname = None
    a_stud = 'active'
    a_book = ''
    div_stud = 'tab-pane active fade in'
    div_book = 'tab-pane fade in'
    if request.method == 'POST':
        select = request.form["select"]
        if select == 'По ученику':
            name = request.form['name']
            surname = request.form['surname']
            grade = request.form['numclass']  # + request.form['letterclass']
            try:
                gender = 1 if request.form['gender'] == 'boy' else 0
            except:
                gender = ''
            if grade in "--":
                grade = ''
            else:
                grade = int(grade)
            puple = executes_for_web.mega_search(Sex=gender, Grade=grade, First_Name=name, Last_Name=surname)
            if puple and len(puple[0]) > 1:
                return render_template('newmain.html', stname='', klass='', arrays=puple,
                                       uch=True, a_book=a_book, a_stud=a_stud, div_book=div_book, div_stud=div_stud,
                                       error='')
            elif len(puple) == 1 and puple[0]:
                return redirect(url_for('student', name=puple[0][0][0] + '_' + puple[0][0][1]))
            else:
                uch = None
                error = "Ничего не найдено"
                a_stud = 'active'
                a_book = ''
                div_stud = 'tab-pane active fade in'
                div_book = 'tab-pane fade in'
                return render_template('newmain.html', stname=name + ' ' + surname, klass='', arrays=[],
                                       error=error, a_book=a_book, a_stud=a_stud, div_book=div_book,
                                       div_stud=div_stud)
        elif select == 'По книге':
            a_stud = ''
            a_book = 'active'
            div_stud = 'tab-pane fade in'
            div_book = 'tab-pane active fade in'
            title = request.form['title'].lower()
            author = request.form['surname'].lower()
            stname = title + ', ' + author
            books = executes_for_web.mega_searchBook(Name_Of_Book=title, Author_Of_Book=author)
            if len(stname) <= 2:
                stname = "Имя не указано"
                return render_template('newmain.html', stname=stname, arrays=None, uch=None,
                                       a_book=a_book, a_stud=a_stud, div_book=div_book, div_stud=div_stud, error='')
            if len(books[0]) > 1:
                uch = False
                return render_template('newmain.html', stname=stname, arrays=books, uch=uch,
                                       a_book=a_book, a_stud=a_stud, div_book=div_book, div_stud=div_stud, error='')
            elif len(books[0]) == 1:
                stname = books[0][0][0][0].upper() + books[0][0][0][1:] + '_' + books[0][0][1].title()
                return redirect(url_for('book', name=stname))
            elif len(books[0]) < 1:
                error = 'Ничего не найдено'
                return render_template('newmain.html', stname=stname, arrays=books, uch=140, a_book=a_book,
                                       a_stud=a_stud, div_book=div_book, div_stud=div_stud, error=error)

    return render_template('newmain.html', stname=None, arrays=None, uch=None,
                           a_book=a_book, a_stud=a_stud, div_book=div_book, div_stud=div_stud, error="")


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('start'))


@app.route('/addbook', methods=['GET', 'POST'])
def addbook():
    variant = 0
    if request.method == 'POST':
        variant = request.form['variant']
        if variant == '0':
            code = request.form['scan']
            cnt = request.form['col']
            try:
                print(int(code))
            except:
                return render_template('add book.html', all_returned='', problem='ISBN должен состоять только из цифр',
                                       variant=variant)
            if len(code) < 13 or len(code) > 13:
                return render_template('add book.html', all_returned='', problem='ISBN должен состоять из 13 цифр',
                                       variant=variant)
            elif len(cnt) < 1 or int(cnt) < 1:
                return render_template('add book.html', all_returned='',
                                       problem='Количество книг не может быть меньше 1', variant=variant)
            else:
                _, name, auth = executes_for_web.Add_Book(code, cnt)
                if _:
                    return render_template('add book.html', all_returned='Добавлено {0}, {1}!'.format(name, auth), problem='', variant=variant)
                else:
                    variant = 1
                    return render_template('add book.html', all_returned='',
                                           problem='Такой книги в общей базе данных нет', variant=variant)
        elif variant == '1':
            name_book = request.form['name_book']
            author_book = request.form['author_book']
            scan = request.form['scan']
            col = request.form['col']
            _, book_name, book_auth = executes_for_web.add_book_f(name_book, author_book, scan, col)
            return render_template('add book.html', all_returned='Добавлено {0}, {1}!'.format(book_name, book_auth), problem='', variant='0')

    return render_template('add book.html', all_returned='', problem='', variant=variant)


@app.route('/get_students', methods=['GET', 'POST'])
def get_students():
    stud = executes_for_web.select_tab(0, 1)

    return render_template('stud.html', stud=stud)


def title(string):
    return ' '.join(list(map(lambda x: x[0].upper() + x[1:], string.split())))


@app.route('/get_books', methods=['GET', 'POST'])
def get_books():
    if request.method == "POST":
        print("Кнопка - ",request.form['btn'])
        num = int(request.form['num']) + 1 if 'Cледующие' in request.form['btn'] else int(request.form['num']) - 10
        books = list(map(lambda x: [x[0], x[1].capitalize(), title(x[2]), x[3], x[4]],
                         list(map(list, executes_for_web.select_tab(1, num)))))
        col = len(books)
        return render_template('book.html', books=books, col=col)
    books = list(map(lambda x: [x[0], x[1].capitalize(), title(x[2]), x[3], x[4]],
                      list(map(list, executes_for_web.select_tab(1, 1)))))
    col = len(books)
    return render_template('book.html', books=books, col=col)


@app.route('/student/<name>', methods=['GET', 'POST'])
def student(name):
    name = tuple(name.split('_'))
    data = executes_for_web.Search_Of_Student(name)
    return render_template('found.html', uch=True, arrays=data, stname=name[0] + ' ' + name[1])


@app.route('/book/<name>', methods=['GET', 'POST'])
def book(name):
    name = tuple(name.split('_'))
    print(name)
    data = executes_for_web.Search_Of_Book(name[0].lower(), name[1].lower())
    if request.method == "POST":
        label =request.form['name']
        author = request.form['author']
        print(label, author)
        executes_for_web.update_BookData(name[0], name[1], label, author)
        return redirect('/book/{0}_{1}'.format(label, author))
    return render_template('found.html', uch=False, arrays=data, stname=name[0] + ', ' + name[1])


app.secret_key = os.urandom(24)

if __name__ == '__main__':
    app.run(debug=True, host="192.168.122.1", port=1111)