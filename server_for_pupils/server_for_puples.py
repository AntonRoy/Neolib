from flask import *
from flask_bootstrap import Bootstrap
import os
import executes_for_web
import Hardware_executes

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def start():
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    usernames = ['1', '2']
    if request.method == 'POST':
        if request.form['login'] in usernames:
            session['logged_in'] = True
            return redirect(url_for('main', id=request.form['login']))
        else:
            error = " Неверный логин/пароль"
    return render_template('about.html', error=error)


@app.route('/main/<id>')
def main(id):
    return render_template('where.html', id=id)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        id_vk = request.form['vk_id']
        gender = request.form['gender']
        name_stud = request.form['name_stud']
        surname_stud = request.form['surname_stud']
        stud = request.form['id_stud']
        grade_stud = request.form['grade_numb'] + request.form['grade_letter']
        # Hardware_executes.registration(name_stud, surname_stud, id_vk, gender, stud, grade_stud)
        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/return_books/<id>', methods=['GET', 'POST'])
def return_books(id):
    returned = ''
    if request.method == 'POST':
        book_isbn = request.form['isbn']
        print(book_isbn, id)
        returned = 'Успешно'
        return render_template('return.html', id=id, returned=returned)
    return render_template('return.html', id=id, returned=returned)


@app.route('/take_books/<id>', methods=['GET', 'POST'])
def take_books(id):
    took = ''
    if request.method == 'POST':
        book_isbn = request.form['isbn']
        print(book_isbn)
        took = "Успешно"
        return render_template('take.html', id=id, took=took)
    return render_template('take.html', id=id, took=took)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('start'))

app.secret_key = os.urandom(24)

if __name__ == '__main__':
    app.run(debug=True)
