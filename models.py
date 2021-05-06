from flask_login import UserMixin
from datetime import datetime
from . import db

class Employee(db.Model, UserMixin):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)  # primary keys are required by SQLAlchemy
    first = db.Column(db.String(20), nullable=True, unique=False)
    last = db.Column(db.String(20),  nullable=True, unique=False)
    username = db.Column(db.String(25))
    passwd = db.Column(db.String(100), nullable=True)

class Room(db.Model):
    room_no = db.Column(db.Integer, autoincrement=True, primary_key=True)
    no_beds = db.Column(db.Integer, nullable=False)
    vacancy = db.Column(db.Integer, nullable=False)
    room_cost = db.Column(db.Integer, nullable=False)

class Guest(db.Model):
    guest_id = db.Column(db.Integer, autoincrement=True, primary_key=True)  # primary keys are required by SQLAlchemy
    firstname = db.Column(db.String(20), nullable = True)
    lastname =db.Column(db.String(20), nullable = True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(10), nullable = True)
    room_no = db.Column(db.Integer, db.ForeignKey('room.room_no'), nullable=False)
    check_in_time = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    total_cost = db.Column(db.Integer, nullable=True)