
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import LONGBLOB



SESSION_SQLALCHEMY = db

class Tickets(db.Model):
    id = db.Column(db.String(36), primary_key=True)  # Set the ID to be a string (UUID)
    description = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(1000))
    comments = db.relationship('Comment', back_populates='ticket')
    status = db.Column(db.String(100))
    create_date = db.Column(db.DateTime)
    complete_date = db.Column(db.DateTime)
    img = db.Column(LONGBLOB)
    name = db.Column(db.String(300))
    assigned_to = db.Column(db.String(1000))
    ticket_type= db.Column(db.String(300))
    ticket_priority= db.Column(db.String(300))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    user_type = db.Column(db.String(150))
    tickets = db.relationship('Tickets')
 
class Comment(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    content = db.Column(db.Text, nullable=False)
    ticket_id = db.Column(db.String(36), db.ForeignKey('tickets.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_fname = db.Column(db.String(150), nullable=False)
    create_date = db.Column(db.DateTime)

    # Specify the correct relationship name in back_populates
    ticket = db.relationship('Tickets', back_populates='comments')


