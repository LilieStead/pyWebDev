from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import db, User
import re

auth = Blueprint('auth', __name__)

# Login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        # Validate email format
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
                login_user(user, remember=True)
                session['user_id'] = user.id
                session['user_email'] = user.email
                session['first_name'] = user.first_Name
                flash('Logged in successfully!', category='success')
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
    session.pop('user_id', None)
    session.pop('user_email', None)
    session.pop('first_name', None)
    flash('Successfully logged out', category='success')
    return redirect(url_for('auth.login'))

# Signup route
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        first_name = request.form.get('firstName', '').strip()
        password1 = request.form.get('password1', '')
        password2 = request.form.get('password2', '')

        # Validate email format
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
            session['user_id'] = new_user.id
            session['user_email'] = new_user.email
            session['first_name'] = new_user.first_Name
            flash('Your account has been created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)


@auth.route('/show_name/<int:user_id>')
@login_required
def show_name(user_id):
    name = get_user_name_by_id(user_id)
    if name:
        return f"User's name is: {name}"
    else:
        return "User not found"
    
    
@auth.route('/usersitems', methods=['GET', 'POST'])
def load_items():
    return render_template("useritems.html", user=current_user)