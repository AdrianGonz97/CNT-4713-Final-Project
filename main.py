

from website import create_app

from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = create_app()

# session is set to expire after 1 day
app.permanent_session_lifetime = timedelta(days=1)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

if __name__ == "__main__":
    db.create_all()
    app.run(debug = True)