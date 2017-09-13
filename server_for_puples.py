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
    if request.method == 'POST':
        if Hardware_executes.true_code(request.form['login']):
            session['logged_in'] = True
            return redirect(url_for('main', id=request.form['login']))
        else:
            error = " Неверный логин/пароль"
    return render_template('about1.html', error=error)


@app.route('/main/<id>')
def main(id):
    return render_template('where1.html', id=id)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        id_vk = request.form['vk_id']
        try:
            id_vk = Hardware_executes.getIdByURL(id_vk)
        except:
            pass
        gender = request.form['gender']
        name_stud = request.form['name_stud']
        surname_stud = request.form['surname_stud']
        stud = request.form['id_stud']
        grade_stud = request.form['grade_numb'] #+ request.form['grade_letter']
        gender = 1 if gender == 'boy' else 0
        Hardware_executes.registration(name_stud, surname_stud, id_vk, gender, stud, grade_stud)
        return redirect(url_for('login'))
    return render_template('signup1.html')


@app.route('/return_books/<id>', methods=['GET', 'POST'])
def return_books(id):
    returned = ''
    if request.method == 'POST':
        book_isbn = request.form['isbn']
        m = Hardware_executes.return_book(id, book_isbn)
        if m:
            m = [m]
        if m[0] and type(m[0]) == bool:
            returned = 'Успешно'
        else:
            returned = m[0][1]
        return render_template('return1.html', id=id, returned=returned)
    return render_template('return1.html', id=id, returned=returned)


@app.route("/profile/<id>", methods=['GET', "POST"])
def profile(id):
    _, name,surname, gender, grade, _, id_gym, id_vk = executes_for_web.getSmeta(id)[0]
    gender = "Мужской" if gender == 1 else "Женский"
    data = executes_for_web.Search_Of_Student([name, surname])
    return render_template("profile.html", name=name+' '+surname, grade=grade, gender=gender,login=id_vk, arrays=data, id=id)


@app.route("/rename/<id>", methods=['GET', "POST"])
def rename(id):
    _, name, surname, gender, grade, _, id_gym, id_vk = executes_for_web.getSmeta(id)[0]
    if request.method == "POST":
        name =request.form['name']
        surname = request.form['surname']
        grade = request.form['grade_numb']
        gender = request.form['gender']
        vk_id = request.form['login']
        executes_for_web.update_data(id, name, surname, gender, grade, vk_id)
        return redirect(url_for('profile', id=id))
    return render_template("rename.html", name=name,surname=surname, grade=grade, gender=gender,login=id_vk, id=id)


@app.route('/take_books/<id>', methods=['GET', 'POST'])
def take_books(id):
    took = ''
    if request.method == 'POST':
        book_isbn = request.form['isbn']
        m = Hardware_executes.take_book(id, book_isbn)
        if m:
            m = [m]
        print(m[0], type(m[0]) == bool)
        if m[0] and type(m[0]) == bool:
            took = 'Успешно'
        return render_template('take1.html', id=id, took=took)
    return render_template('take1.html', id=id, took=took)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('start'))

app.secret_key = os.urandom(24)

if __name__ == '__main__':
    app.run(host='192.168.122.1', port=2222)