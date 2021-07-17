import os
import string
import random
import hashlib

from dotenv import load_dotenv
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

# loads the secret for encryption from environment vars
load_dotenv()
SERVER_SECRET = os.getenv('SERVER_SECRET')

app = Flask(__name__)
app.secret_key = SERVER_SECRET
# session is set to expire after 1 day
app.permanent_session_lifetime = timedelta(days=1)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# SQL model for a user
class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.LargeBinary(32))
    email = db.Column(db.String(100))
    token = db.Column(db.String(100))
    streamkey = db.Column(db.String(25))

    def __init__(self, username, password, email, token):
        self.username = username
        self.password = password
        self.email = email
        self.token = token
        # generates a random stream key
        letters = string.ascii_letters
        self.streamkey = ''.join(random.choice(letters) for i in range(25))

# routes to home page
@app.route("/")
def home():
    return render_template("index.html")

# user login page
@app.route("/login", methods=['POST', "GET"])
def login():
    if request.method == "POST":
        # required for the session lifetime to function
        session.permanent = True
        # pulls the user credentials from the request
        username = request.form["username"]
        password = request.form["password"]
        # check if the user exists in the db
        found_user = users.query.filter_by(username=username).first()
        if found_user:
            # if user found, check credentials
            if check_password(password, found_user.password):
                session["username"] = found_user.username
                session["streamkey"] = found_user.streamkey
                # creates a session for the user
                session["username"] = username
                flash("You have successfully logged in!")
                return redirect(url_for("dashboard"))
            else: # if the passwords don't match
                flash("Username and password do not match!")
                return redirect(url_for("login"))
        else: # if the username dne
            flash("Username does not exist!")
            return redirect(url_for("login"))        
    else:
        # route to dashboard if user is already logged in 
        if "username" in session and "streamkey" in session:
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html")

# user logout page
@app.route("/logout")
def logout():
    if "username" in session:
        username = session["username"]
        session.pop("username", None)
        session.pop("streamkey", None)
        flash(f"You have logged out as {username}!", "info")
    return redirect(url_for("login"))

# user registration page
@app.route("/register", methods=['POST', "GET"])
def register():
    if request.method == "POST":
        password = request.form["password"]
        repassword = request.form["repassword"]
        # if the passwords match..
        if repassword == password:
            username = request.form["username"]
            # and if the pass or username is not blank or empty
            if password and password.strip() and username and username.strip():
                # check if the user already exists in the db
                found_user = users.query.filter_by(username=username).first()
                if found_user: # if the user already exists..
                    flash("Username already exists!")
                    return redirect(url_for("register"))
                else:
                    # success! hash password and create a user model
                    hashed_pass = hash_password(password) # hashes password
                    user = users(username, hashed_pass, "", "")
                    # adds user to the db and commits
                    db.session.add(user)
                    db.session.commit()
                    flash("You have successfully registered!")
                    return redirect(url_for("login"))
            else:
                flash("The passwords and usernames cannot be blank!")
                return redirect(url_for("register"))
        else: # if they don't match..
            flash("The passwords do not match!")
            return redirect(url_for("register"))
    else: # otherwise, send to page
        return render_template("register.html")

# user dashboard page
@app.route("/dashboard")
def dashboard():
    # if a user already has a session..
    if "username" in session and "streamkey" in session:
        # route user to dashboard
        username = session["username"]
        streamkey = session["streamkey"]
        return render_template("dashboard.html", username=username, streamkey=streamkey)
    else: # otherwise, send to login
        flash("You need to be logged in to access the dashboard!")
        return redirect(url_for("login"))

# routes to the about page
@app.route("/about")
def about():
    return render_template("about.html")

# routes to the requirements page
@app.route("/requirements")
def requirements():
    return render_template("requirements.html")

# hashes the password and returns the unicode to store
def hash_password(password):
    salt = os.urandom(16) # generates the salt
    key = hashlib.pbkdf2_hmac(
        'sha256', # hash algorithm
        password.encode('utf-8'), # converts pass to bytes
        salt, 
        100000 # num of iterations
    )
    return salt + key

# checks hashed password vs the provided password
def check_password(password, stored_password):
    salt = stored_password[:16] # length of salt
    key = stored_password[16:]
    new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return key == new_key

if __name__ == "__main__":
    db.create_all()
    app.run(debug = True)