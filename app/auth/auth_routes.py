from flask import render_template, flash, redirect, url_for, request
from app import db
from app.auth import auth_blueprint as bp_auth
import sqlalchemy as sqla
from app.main.models import User, Student
from app.auth.auth_forms import LoginForm
from flask_login import login_user, current_user, logout_user, login_required


@bp_auth.route('/user/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.user_type == 'Student':
            return redirect(url_for('main.student_index'))
        else:
            return redirect(url_for('main.instructor_index'))

    lform = LoginForm()

    if request.method == 'POST':
        if lform.validate_on_submit():
            query = sqla.select(User).where(User.username == lform.username.data)
            user = db.session.scalars(query).first()

            if (user is None) or(user.get_password(lform.password.data) == False):
                flash('Invalid username or password')
                return redirect(url_for('auth.login'))
            login_user(user, remember=lform.remember_me.data)
            if current_user.user_type=='Student':
                return redirect(url_for('main.student_index'))
            else:
                return redirect(url_for('main.instructor_index'))

    return render_template('login.html', form = lform)

@bp_auth.route('/user/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))