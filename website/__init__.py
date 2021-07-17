import os

from dotenv import load_dotenv
from flask import Flask

# loads the secret for encryption from environment vars
load_dotenv()
SERVER_SECRET = os.getenv('SERVER_SECRET')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SERVER_SECRET

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    
    return app