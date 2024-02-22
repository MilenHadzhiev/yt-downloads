import re
from re import compile, fullmatch  # pylint: disable=redefined-builtin

from flask import request, flash


regex = compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')


def validate_personal_data(user, is_login: bool) -> bool:  # pylint: disable=unused-argument
    email = request.form.get('email')
    password1 = request.form.get('password1')
    if not fullmatch(regex, email):
        flash('Email is incorrect format', category='error')
        return False

    if is_login:
        return validate_login_data(user, password1)
    return validate_signup_data(user, password1)


def validate_login_data(user, password: str) -> bool:
    if not user:
        flash('No user found', category='error')
        return False
    if not user.check_password(password):
        flash('Wrong password', category='error')
        return False
    return True


def validate_signup_data(user, password: str) -> bool:
    if user:
        flash(f'User with email:{user.email} already exists', category='error')
        return False

    if password != request.form.get('password2'):
        flash('Passwords must match', category='error')
        return False

    return True


def validate_url(url: str) -> bool:
    pattern = re.compile(r'^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+')
    return bool(fullmatch(pattern, url))
