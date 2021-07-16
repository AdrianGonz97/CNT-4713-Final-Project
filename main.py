import os
from flask import Flask, redirect, url_for, render_template, request, session
from dotenv import load_dotenv

load_dotenv()
SERVER_SECRET = os.getenv('SERVER_SECRET')

app = Flask(__name__)
app.secret_key = SERVER_SECRET

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=['POST', "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        # password = request.form["password"]
        session["user"] = username
        return redirect(url_for("dashboard"))
    else:
        if "user" in session:
            return redirect(url_for("dashboard"))
        
        return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/requirements")
def requirements():
    return render_template("requirements.html")

@app.route("/dashboard")
def dashboard():
    if "user" in session:
        user = session["user"]
        return render_template("dashboard.html", username=user)
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug = True)