from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import db, User
import re


auth = Blueprint('auth', __name__)

# Login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()

        # Correctly indented email format validation
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_regex, email):
            flash('Invalid email format. Please enter a valid email.', category='danger')
            return render_template("login.html", user=current_user)

        if not email or not password:
            flash('Please fill in both fields.', category='danger')
            return render_template("login.html", user=current_user)

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

# Logout route
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('successfully logged out', category='success')
    return redirect(url_for('auth.login'))

# Signup route
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_regex, email):
            flash('Invalid email format. Please enter a valid email.', category='danger')
            return render_template("signup.html", user=current_user)


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
