import sqlite3

from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///WaterGarden.db"
app.config["SECRET_KEY"] = "abc"
db = SQLAlchemy()


login_manager = LoginManager()
login_manager.init_app(app)


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)


db.init_app(app)

with app.app_context():
    db.create_all()


@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        #print(generate_password_hash(request.form.get("password")))
        #pass_hash = generate_password_hash(request.form.get("password"))
        user = Users(username=request.form.get("username"),
                     password=generate_password_hash(request.form.get("password")))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("sign_up.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(
            username=request.form.get("username")).first()
        print(user.password)
        print(generate_password_hash(request.form.get("password")))
        if check_password_hash(user.password, request.form.get("password")):
            login_user(user)
            return redirect(url_for("home"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route('/registration', methods=['GET', 'POST'])
def form_registration():

   if request.method == 'POST':
       Login = request.form.get('Login')
       Password = request.form.get('Password')

       db_lp = sqlite3.connect('instance/WaterGarden.db')
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

        db_lp = sqlite3.connect('instance/WaterGarden.db')
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