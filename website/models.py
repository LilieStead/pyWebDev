from . import db
from flask_login import UserMixin

# Association table linking users and products (many-to-many)
user_product_association = db.Table(
    'user_product',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_Name = db.Column(db.String(150))  # ✅ Matches `signup` function
    # Many-to-many relationship with Product
    products = db.relationship('Product', secondary=user_product_association, backref='users')

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(1000), nullable=False)
    title = db.Column(db.String(300))
    description = db.Column(db.Text)
    price = db.Column(db.String(100))  # Current/latest price
    last_price = db.Column(db.String(100))  # Previous price