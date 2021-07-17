from . import db
import random
import string

# SQL model for a User
class User(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.LargeBinary(32))
    email = db.Column(db.String(100))
    token = db.Column(db.String(100))
    streamkey = db.Column(db.String(25), unique=True)

    def __init__(self, username, password, email, token):
        self.username = username
        self.password = password
        self.email = email
        self.token = token
        # generates a random stream key
        letters = string.ascii_letters
        self.streamkey = ''.join(random.choice(letters) for i in range(25))