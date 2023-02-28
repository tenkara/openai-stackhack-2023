from flask import Flask, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Line below only required once, wheen creating DB


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True ,unique=True)
    password_hash = db.Column(db.String(64))
    email = db.Column(db.String(64), index=True, unique=True)

#Line below only required once, wheen creating DB
#db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def home():
    return 'hello world'

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password_hash = generate_password_hash(request.form['password'], method='pbkdf2:sha256', salt_length=8)
        email = request.form['email']
        
        # check if user already exists
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists')
            return "Username already exists"
        
        new_user = User(username=username, password_hash=password_hash, email=email)
        db.session.add(new_user)
        db.session.commit()
        return "user created"
    return "signup"

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # check if user already exists
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password_hash, password):
                return "Logged in"
            else:
                return "Incorrect password"
        else:
            return "User does not exist"
    return "login"


if __name__ == '__main__':
    app.run(debug=True)
