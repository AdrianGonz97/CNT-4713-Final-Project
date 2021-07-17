import os
from dotenv import load_dotenv
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta

# loads the secret for encryption from environment vars
load_dotenv()
SERVER_SECRET = os.getenv('SERVER_SECRET')

app = Flask(__name__)
app.secret_key = SERVER_SECRET
# session is set to expire after 1 day
app.permanent_session_lifetime = timedelta(days=1)

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
        # creates a session for the user
        session["user"] = username
        flash("You have successfully logged in!")
        return redirect(url_for("dashboard"))
    else:
        # route to dashboard if user is already logged in 
        if "user" in session:
            return redirect(url_for("dashboard"))
        
        return render_template("login.html")

# user logout page
@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        session.pop("user", None)
        flash(f"You have logged out as {user}!", "info")
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
                # perform the registration
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
    if "user" in session:
        # route user to dashboard
        user = session["user"]
        return render_template("dashboard.html", username=user)
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

if __name__ == "__main__":
    app.run(debug = True)