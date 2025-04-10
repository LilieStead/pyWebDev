from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

# This is now your public landing page — always accessible
@views.route('/')
def landing():
    return render_template("landing.html", user=current_user)

# This is the actual home page for logged-in users
@views.route('/home')
@login_required
def home():
    return render_template("home.html", user=current_user)