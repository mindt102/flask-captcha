from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User
from flask_login import login_user, login_required, logout_user
from . import db
from flask_bcrypt import generate_password_hash, check_password_hash
from .forms.LoginForm import LoginForm
from .forms.SignupForm import SignupForm

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    login_form = LoginForm()
    return render_template('login.html', form=login_form)


@auth.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    login_form = LoginForm()

    if not login_form.validate_on_submit():
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    username = login_form.username.data
    password = login_form.password.data

    # remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=username).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        # if the user doesn't exist or password is wrong, reload the page
        return redirect(url_for('auth.login'))

    login_user(user)
    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    signup_form = SignupForm()
    return render_template('signup.html', form=signup_form)


@auth.route('/signup', methods=['POST'])
def signup_post():
    signup_form = SignupForm()
    # code to validate and add user to database goes here
    # print(username, password)
    # print(signup_form.errors)

    # if signup_form.is_submitted():
    #     print("submitted")

    # if signup_form.validate():
    #     print("valid")

    # print(signup_form.errors)
    # print(signup_form.validate_on_submit())
    if not signup_form.validate_on_submit():
        flash('Please check your sign up details and try again')
        return redirect(url_for('auth.signup'))

    username = signup_form.username.data
    password = signup_form.password.data

    # if this returns a user, then the email already exists in database
    user = User.query.filter_by(username=username).first()

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Username already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(username=username,
                    password=generate_password_hash(password))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
