from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path, getenv

# loads the secret for encryption from environment vars
load_dotenv()
SERVER_SECRET = getenv('SERVER_SECRET')
DB_NAME = getenv('DB_NAME')

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SERVER_SECRET
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User
    create_db(app)

    return app

def create_db(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print("New database created!")