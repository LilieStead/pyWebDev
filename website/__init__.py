from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'  # Change this in production!
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # Register Blueprints without '/auth' prefix
    from .views import views
    from .auth import auth  # Import the auth blueprint here
    app.register_blueprint(views, url_prefix='/')  # Register views blueprint
    app.register_blueprint(auth)  # Remove the '/auth' prefix here

    # Import models (no more Note)
    from .models import User, Product
    create_database(app)  # Create the database by calling this function

    # Login manager setup
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# Define the create_database function here
def create_database(app):
    with app.app_context():
        if not path.exists('website/' + DB_NAME):
            db.create_all()
            print('Created Database!')
