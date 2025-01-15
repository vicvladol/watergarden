import sqlite3
from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/registration', methods=['GET', 'POST'])
def form_registration():

   if request.method == 'POST':
       Login = request.form.get('Login')
       Password = request.form.get('Password')

       db_lp = sqlite3.connect('WaterGarden.db')
       cursor_db = db_lp.cursor()
       sql_insert = '''INSERT INTO users VALUES('{}','{}');'''.format(Login, Password)

       cursor_db.execute(sql_insert)
       db_lp.commit()

       cursor_db.close()
       db_lp.close()

       return render_template('successfulregis.html')

   return render_template('registration.html')


@app.route('/authorization', methods=['GET', 'POST'])
def form_authorization():
    if request.method == 'POST':
        Login = request.form.get('Login')
        Password = request.form.get('Password')

        db_lp = sqlite3.connect('WaterGarden.db')
        cursor_db = db_lp.cursor()
        cursor_db.execute(f"SELECT password FROM users WHERE login = '{Login}';")
        pas = cursor_db.fetchall()

        cursor_db.close()
        try:
            if pas[0][0] != Password:
                return render_template('auth_bad.html')
        except:
            return render_template('auth_bad.html')

        db_lp.close()
        return render_template('successfulauth.html')

    return render_template('authorization.html')

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()