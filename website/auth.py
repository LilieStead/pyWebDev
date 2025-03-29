from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "<p>logout</p>"

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':  # Check if the form is submitted
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')



        # Add all val in here !

        if len(email) < 4:  # Ensure email is longer than 3 characters
            flash('Email must be greater than 3 characters.', category='danger')
        elif len(firstName) < 2:  # Ensure first name is longer than 1 character
            flash('First name must be greater than 1 character.', category='danger')
        elif password1 != password2:  # Check if passwords match
            flash('Your passwords do not match.', category='danger')
        elif len(password1) < 7:  # Ensure password is at least 7 characters
            flash('Your password needs to be at least 7 characters.', category='danger')
        else:
            flash('Your account has been created!', category='success')

    return render_template("signup.html")
