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
        flash("You need to be logged in to access the dashboard!", category="error")
        return redirect(url_for("auth.login"))

# routes to the about page
@views.route("/about")
def about():
    return render_template("about.html")

# routes to the requirements page
@views.route("/requirements")
def requirements():
    return render_template("requirements.html")

# logged in users can routes to the video page to view static files
@views.route("/videos/<video_id>")
def video(video_id):
    # if the user is logged in
    if "username" in session and "streamkey" in session:
        # route user to video
        return render_template("video.html", video_id=video_id)
    else: # otherwise, send to login
        flash("You need to be logged in to access videos!", category="error")
        return redirect(url_for("auth.login"))

# logged in users can route to the active streams page
@views.route("/streams")
def streams():
    # if the user is logged in
    if "username" in session and "streamkey" in session:
        # route user to active streams menu
        return render_template("stream-menu.html")
    else: # otherwise, send to login
        flash("You need to be logged in to access live streams!", category="error")
        return redirect(url_for("auth.login"))

# logged in users can route a user's live stream page
@views.route("/user/<streamer_username>")
def user_stream(streamer_username):
    # if the user is logged in
    if "username" in session and "streamkey" in session:
        # route user streamer's live stream
        return render_template("stream-menu.html")
    else: # otherwise, send to login
        flash("You need to be logged in to access live streams!", category="error")
        return redirect(url_for("auth.login"))