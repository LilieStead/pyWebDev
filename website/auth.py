from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db  # Import db instance from __init__.py
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Please fill in both fields.', category='danger')
            return render_template("login.html")

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect, please try again!', category='danger')
        else:
            flash('User does not exist', category='danger')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('User already exists', category='danger')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='danger')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='danger')
        elif password1 != password2:
            flash('Your passwords do not match.', category='danger')
        elif len(password1) < 7:
            flash('Your password needs to be at least 7 characters.', category='danger')
        else:
            hashed_password = generate_password_hash(password1, method='pbkdf2:sha256')

            new_user = User(email=email, first_Name=first_name, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Your account has been created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)
