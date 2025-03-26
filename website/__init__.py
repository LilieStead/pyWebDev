from flask import Flask  # ✅ Correct import

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'

    return app