from flask import *
from flask_bootstrap import Bootstrap
import os
import executes_for_web
import Hardware_executes

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
        try:
            if request.form['login'] == username and request.form['password'] == password:
                session['logged_in'] = True
                return redirect(url_for('main'))
            else:
                error = " Неверный логин/пароль"
        except:
            result='Успешно!'
            numb_form = request.form['numb_form']
            print(numb_form)
            if numb_form == '0':
                # если пользователь регистрируется
                id_vk = request.form['vk_id']
                gender = request.form['gender']
                name_stud = request.form['name_stud']
                surname_stud = request.form['surname_stud']
                stud = request.form['id_stud']
                grade_stud = request.form['grade_numb'] + request.form['grade_letter']
                Hardware_executes.registration(name_stud, surname_stud, id_vk, gender, stud, grade_stud)

            elif numb_form == '1':
                # если пользователь забирает книгу
                isbn = request.form['book_id']
                stud = request.form['id_stud']
                ids = Hardware_executes.login2id(stud)
                idb = Hardware_executes.isbn2id(isbn)
                print(ids, idb)
                Hardware_executes.take_book(ids, idb)
            elif numb_form == '2':
                # если пользователь возвращает книгу
                stud = request.form['id_stud']
                isbn = request.form['book_id']
                ids = Hardware_executes.login2id(stud)
                idb = Hardware_executes.isbn2id(isbn)
                Hardware_executes.return_book(ids, idb)
            return render_template('about.html', error='', result=result)
    return render_template('about.html', error=error, result='')


@app.route('/main', methods=['GET', 'POST'])
def main():
    stname = None
    a_stud = 'active'
    a_book = ''
    div_stud = 'tab-pane active fade in'
    div_book = 'tab-pane fade in'
    if request.method == 'POST':
        try:
            selectedStud = request.form['stud']
            types = request.form['type']
            if types:
                uch = True
                print(list(map(lambda x: x[1:-1], selectedStud[1:-1].split(', '))))
                data = executes_for_web.Search_Of_Student(list(map(lambda x: x[1:-1], selectedStud[1:-1].split(', '))))
                stname = list(map(lambda x: x[1:-1], selectedStud[1:-1].split(', ')))
            else:
                a_stud = ''
                a_book = 'active'
                div_stud = 'tab-pane fade in'
                div_book = 'tab-pane active fade in'
                uch = False
                selectedStud = selectedStud[1:-1].split(', ')
                print(selectedStud)
                data = executes_for_web.Search_Of_Book(selectedStud[1], selectedStud[0])
            print('выбранный: ', selectedStud, types)
            print(1)
            return render_template('found.html', stname=stname[0] + ' ' + stname[1], arrays=data, uch=uch)
        except:
            select = request.form["select"]
            print(select)
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
                if len(puple[0]) > 1:
                    return render_template('newmain.html', stname=name + ' ' + surname, klass=grade, arrays=puple,
                                           uch=True, a_book=a_book, a_stud=a_stud, div_book=div_book, div_stud=div_stud,
                                           error='')
                elif len(puple) == 1 and puple[0]:
                    books = executes_for_web.Search_Of_Student(puple[0][0])
                    return render_template('found.html', stname=name + ' ' + surname, klass=grade, arrays=books)
                else:
                    uch = None
                    error = "Ничего не найдено"
                    a_stud = 'active'
                    a_book = ''
                    div_stud = 'tab-pane active fade in'
                    div_book = 'tab-pane fade in'
                    return render_template('newmain.html', stname=name + ' ' + surname, klass=grade, arrays=[],
                                           error=error, a_book=a_book, a_stud=a_stud, div_book=div_book,
                                           div_stud=div_stud)
            elif select == 'По книге':
                a_stud = ''
                a_book = 'active'
                div_stud = 'tab-pane fade in'
                div_book = 'tab-pane active fade in'
                title = request.form['title']
                author = request.form['surname']
                stname = title + ', ' + author
                students = executes_for_web.mega_searchBook(Name_Of_Book=title, Author_Of_Book=author)
                if len(stname) <= 2:
                    stname = "Имя не указано"
                    return render_template('newmain.html', stname=stname, arrays=None, uch=None,
                                           a_book=a_book, a_stud=a_stud, div_book=div_book, div_stud=div_stud, error='')
                print('ученики: ', students)
                if len(students[0]) > 1:
                    uch = False
                    return render_template('newmain.html', stname=stname, arrays=students, uch=uch,
                                           a_book=a_book, a_stud=a_stud, div_book=div_book, div_stud=div_stud, error='')
                elif len(students[0]) == 1:
                    uch = False
                    print(students)
                    data = executes_for_web.Search_Of_Book(students[0][0][0], students[0][0][1])
                    print(stname, data)
                    return render_template('found.html', stname=stname, arrays=data, uch=uch)
                elif len(students[0]) < 1:
                    error = 'Ничего не найдено'
                    return render_template('newmain.html', stname=stname, arrays=students, uch=140, a_book=a_book,
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
        print(variant)
        if variant == '0':
            code = request.form['scan']
            cnt = request.form['col']
            print(code, cnt)
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
                add = executes_for_web.Add_Book(code, cnt)
                if add:
                    return render_template('add book.html', all_returned='Добавлено!', problem='', variant=variant)
                else:
                    variant = 1
                    return render_template('add book.html', all_returned='',
                                           problem='Такой книги в общей базе данных нет', variant=variant)
        elif variant == '1':
            print("мы здесь")
            name_book = request.form['name_book']
            author_book = request.form['author_book']
            scan = request.form['scan']
            col = request.form['col']
            print(name_book, author_book, scan, col)
            return render_template('add book.html', all_returned='Добавлено!', problem='', variant='0')

    return render_template('add book.html', all_returned='', problem='', variant=variant)


@app.route('/get_students', methods=['GET', 'POST'])
def get_students():
    stud = executes_for_web.select_tab(0)

    return render_template('stud.html', stud=stud)


def title(string):
    return ' '.join(list(map(lambda x: x[0].upper() + x[1:], string.split())))


@app.route('/get_books', methods=['GET', 'POST'])
def get_books():
    books = list(map(lambda x: [x[0], x[1], x[2], title(x[3]), title(x[4])],
                      list(map(list, executes_for_web.select_tab(1)))))

    return render_template('book.html', books=books)


@app.route('/student/<name>', methods=['GET', 'POST'])
def student(name):
    name = tuple(name.split('_'))
    data = executes_for_web.Search_Of_Student(name)
    return render_template('found.html', uch=True, arrays=data, stname=name[0] + ' ' + name[1])


@app.route('/book/<name>', methods=['GET', 'POST'])
def book(name):
    name = tuple(name.split('_'))
    data = executes_for_web.Search_Of_Book(name[0].lower(), name[1].lower())
    return render_template('found.html', uch=False, arrays=data, stname=name[0] + ', ' + name[1])


app.secret_key = os.urandom(24)

if __name__ == '__main__':
    app.run(debug=True)