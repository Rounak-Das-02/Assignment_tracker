from . import db
from flask_login import UserMixin
from datetime import datetime


class User(db.Model , UserMixin):
    id = db.Column(db.Integer , primary_key = True)
    email = db.Column(db.String(100) , unique = True)
    password = db.Column(db.String)
    name =  db.Column(db.String(100))
    assignments = db.relationship('Assignment' , backref = "author" , lazy = True)



class Assignment(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    assignment = db.Column(db.String)
    date_posted = db.Column(db.DateTime , default = datetime.now())

    due_date = db.Column(db.DateTime , default = datetime.now())
    comment = db.Column(db.String)
    completion = db.Column(db.Boolean , default = False)

    user_id = db.Column(db.Integer , db.ForeignKey("user.id") , nullable = False)

