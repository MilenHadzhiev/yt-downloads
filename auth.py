from flask import Blueprint, render_template, request, flash, redirect, url_for
from backend.validations import validate_personal_data
from werkzeug.security import generate_password_hash
from models import User
from flask_login import login_user, login_required, logout_user
auth = Blueprint('auth', __name__)
from backend.setup import db

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        if not validate_personal_data(data, is_login=True):
            return render_template('login.html')
        email = data.get('email')
        user = User.query.filter_by(email=email).first()
        login_user(user, remember=True)
        return redirect(url_for('views.homepage'))
    return render_template('login.html', name='Pe60')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        data = request.form
        if not validate_personal_data(data, is_login=False):
            # TODO
            return render_template('sign_up.html')
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password1 = generate_password_hash(request.form.get('password1'), method='sha256')
        new_user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=password1
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash('Account created', category='info')
        return redirect(url_for('views.homepage'))
    return render_template('sign_up.html')