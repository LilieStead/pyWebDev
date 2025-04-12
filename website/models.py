from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_Name = db.Column(db.String(150))

    # One-to-one relationship with Product
    product = db.relationship('Product', backref='user', uselist=False)  # uselist=False makes it a one-to-one

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(1000), nullable=False)
    title = db.Column(db.String(300))
    description = db.Column(db.Text)
    price = db.Column(db.String(100))       # Current/latest price
    last_price = db.Column(db.String(100))  # Previous price

    # Foreign key for the user this product belongs to
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # One-to-one, product belongs to one user
