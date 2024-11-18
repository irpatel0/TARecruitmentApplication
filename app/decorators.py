from functools import wraps
from flask import g, redirect, url_for, render_template, flash
from flask_login import current_user

def role_required(role):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if current_user.user_type != role:
                flash(f'You are not allowed to access {role} Page')
                return redirect(url_for('auth.login'))
            return func(*args, **kwargs)
        return decorated_function
    return decorator