from enum import unique
from flask_sqlalchemy import SQLAlchemy
from werkzeug import security
import datetime

db = SQLAlchemy()

# a model of a user for the database
class User (db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(50))
    password = db.Column(db.String, unique=True)
    household = db.Column(db.String(20))
    balance = db.Column(db.Float)

    def __init__ (self, name, email, password, household, balance):
        self.name = name
        self.email = email
        self.password = password
        self.household = household
        self.balance = balance

class Household (db.Model):
    __tablename__ = 'households'
    name = db.Column(db.String(20), unique = True, primary_key = True)

    def __init__ (self, name):
        self.name = name

# a model of s Bill for the database
class Bill (db.Model):
    __tablename__="Bills"
    bill_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), unique=True)
    amount = db.Column(db.Float)
    user_id = db.Column(db.Integer)
    deadline = db.Column(db.String(20))

    def __init__(self, name, amount, deadline, user_id):
        self.name = name
        self.amount = amount
        self.deadline = deadline
        self.user_id = user_id

class SharedBill (db.Model):
    __tablename__ = "SharedBill"
    shared_id=db.Column(db.Integer, primary_key=True)
    bill_id = db.Column(db.Integer, db.ForeignKey('Bills.bill_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    paid = db.Column(db.Boolean)

    def __init__(self, bill_id, user_id, paid):
        self.bill_id=bill_id 
        self.user_id=user_id
        self.paid = paid

class Image (db.Model):
    __tablename__ = 'images'
    image_id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.Text())
    bill_id = db.Column(db.Integer)

    def __init__ (self, filename, bill_id):
        self.filename = filename
        self.bill_id = bill_id

def dbinit():
    bills = Bill.query.all()
    users = len(User.query.all())
    for b in bills:
        for _ in range(users):
            db.session.add(SharedBill(bill_id=b.bill_id, user_id=b.user_id, paid=False))
    db.session.commit()