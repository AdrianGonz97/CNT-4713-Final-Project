import os
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SERVER_SECRET')
    return app