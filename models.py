from extension import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),unique=True,nullable=False)
    email=db.Column(db.String(50),unique=True,nullable=False)
    hash_password=db.Column(db.String(100),nullable=False)
    balance=db.Column(db.Float(),default=10000.0)
    print("models imported")
    def set_password(self,password):
        self.hash_password=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.hash_password,password)    