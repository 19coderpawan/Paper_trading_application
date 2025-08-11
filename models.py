from extension import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime,timezone

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),unique=True,nullable=False)
    email=db.Column(db.String(50),unique=True,nullable=False)
    hash_password=db.Column(db.String(100),nullable=False)
    balance=db.Column(db.Float(),default=10000.0)

  # Relationships
    portfolio=db.relationship('Portfolio',backref='owner',lazy=True)
    transaction=db.relationship('Transaction',backref='owner',lazy=True)
   
    def set_password(self,password):
        self.hash_password=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.hash_password,password)    
    
class Portfolio(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False) #ref to User table.
    symbol=db.Column(db.String(20),nullable=False)
    quantity=db.Column(db.Float,nullable=False,default=0.0)
    avg_price=db.Column(db.Float,nullable=False,default=0.0)
    created_at=db.Column(db.DateTime,default=lambda:datetime.now(timezone.utc))
    updated_at=db.Column(db.DateTime,default=lambda:datetime.now(timezone.utc),onupdate=lambda:datetime.now(timezone.utc))

class Transaction(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    symbol=db.Column(db.String(20),nullable=False)
    quantity=db.Column(db.Float,nullable=False,default=0.0)
    price=db.Column(db.Float,nullable=False,default=0.0)
    transaction_type=db.Column(db.String(4),nullable=False)
    timestamp=db.Column(db.DateTime,default=lambda:datetime.now(timezone.utc))