import re
from re import compile, fullmatch
from werkzeug.datastructures import ImmutableMultiDict
from flask import request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
regex = compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

def validate_personal_data(data: ImmutableMultiDict, is_login: bool) -> bool:
    email = request.form.get('email')
    password1 = request.form.get('password1')
    if not fullmatch(regex, email):
        flash('Email is incorrect format', category='error')
        return False

    user = User.query.filter_by(email=email).first()
    if is_login:
        return validate_login_data(user, password1)

    return validate_signup_data(user, password1)

def validate_login_data(user: User, password: str) -> bool:
    if not user:
        flash('No user found', category='error')
        return False
    if not user.check_password(password):
        flash('Wrong password', category='error')
        return False
    return True

def validate_signup_data(user: User, password: str) -> bool:
    if user:
        flash(f'User with email:{user.email} already exists', category='error')
        return False

    if password != request.form.get('password2'):
        flash('Passwords must match', category='error')
        return False

    return True

def validate_url(url: str) -> bool:
    pattern = re.compile(r'^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+')
    return True if fullmatch(pattern, url) else None