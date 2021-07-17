import hashlib

from flask import Blueprint, Flask, redirect, url_for, render_template, request, session, flash
from . import db
from .models import User

auth = Blueprint('auth', __name__)

# user login page
@auth.route("/login", methods=['POST', "GET"])
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
                flash("You have successfully logged in!", category="success")
                return redirect(url_for("views.dashboard"))
            else: # if the passwords don't match
                flash("Username and password do not match!", category="error")
                return redirect(url_for("auth.login"))
        else: # if the username dne
            flash("Username does not exist!", category="error")
            return redirect(url_for("auth.login"))        
    else:
        # route to dashboard if user is already logged in 
        if "username" in session and "streamkey" in session:
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html")

# user logout page
@auth.route("/logout")
def logout():
    if "username" in session:
        username = session["username"]
        session.pop("username", None)
        session.pop("streamkey", None)
        flash(f"You have logged out as {username}!", category="info")
    return redirect(url_for("auth.login"))

# user registration page
@auth.route("/register", methods=['POST', "GET"])
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
                    flash("Username already exists!", category="error")
                    return redirect(url_for("auth.register"))
                else:
                    # success! hash password and create a user model
                    hashed_pass = hash_password(password) # hashes password
                    user = User(username, hashed_pass, "", "")
                    # adds user to the db and commits
                    db.session.add(user)
                    db.session.commit()
                    flash("You have successfully registered!", category="success")
                    return redirect(url_for("auth.login"))
            else:
                flash("The passwords and usernames cannot be blank!", category="error")
                return redirect(url_for("auth.register"))
        else: # if they don't match..
            flash("The passwords do not match!", category="error")
            return redirect(url_for("auth.register"))
    else: # otherwise, send to page
        return render_template("register.html")

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