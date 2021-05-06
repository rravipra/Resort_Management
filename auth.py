from flask import abort, flash, Flask, jsonify, render_template, request, Blueprint, redirect, url_for
from flask_login import login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import generate_password_hash, check_password_hash
from .models import Employee
import yaml
from .import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    employee = Employee.query.filter_by(username=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    print(f'employee.passwd {employee.passwd}')
    print(f'password {password}')
    if not employee or not check_password_hash(employee.passwd, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))  # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(employee, remember=remember)
    return redirect(url_for('main.index'))


@auth.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():

    email = request.form.get('email')
    firstname = request.form.get('firstname')
    lastname= request.form.get('lastname')
    password = request.form.get('password')

    # if this returns a user, then the email already exists in database
    employee = Employee.query.filter_by(username=email).first()

    print(employee)

    if employee:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.login'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_employee = Employee(username=email, first=firstname, last=lastname, passwd=generate_password_hash(password))

    # add the new user to the database
    db.session.add(new_employee)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))