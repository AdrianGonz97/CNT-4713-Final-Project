from flask import Blueprint, Flask, redirect, url_for, render_template, session, flash

views = Blueprint('views', __name__)

# routes to home page
@views.route("/")
def home():
    return render_template("index.html")

# user dashboard page
@views.route("/dashboard")
def dashboard():
    # if a user already has a session..
    if "username" in session and "streamkey" in session:
        # route user to dashboard
        username = session["username"]
        streamkey = session["streamkey"]
        return render_template("dashboard.html", username=username, streamkey=streamkey)
    else: # otherwise, send to login
        flash("You need to be logged in to access the dashboard!", category="success")
        return redirect(url_for("auth.login"))

# routes to the about page
@views.route("/about")
def about():
    return render_template("about.html")

# routes to the requirements page
@views.route("/requirements")
def requirements():
    return render_template("requirements.html")

@views.route("/videos/<video_id>")
def videos(video_id):
    return render_template("videos.html", video_id=video_id)