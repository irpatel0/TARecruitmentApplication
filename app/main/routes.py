from flask import render_template, flash, redirect, url_for, request, jsonify
import sqlalchemy as sqla
from app import db
from app.main import main_blueprint as bp_main
from flask_login import current_user, login_required
from app.decorators import role_required
from app.main.models import Course, Position,  CourseSection


@bp_main.route('/', methods=['GET'])
@bp_main.route('/index', methods=['GET'])
def index():
    return redirect(url_for('auth.login'))

@bp_main.route('/student_index', methods=['GET'])
@login_required
@role_required('Student')
def student_index():
    positions = db.session.query(Position).all()
    if current_user.user_type != 'Student':
        flash('You are not allowed to access Student Page')
        return redirect(url_for('auth.login'))
    return render_template('student_index.html', positions = positions)

@bp_main.route('/instructor_index', methods=['GET'])
@login_required
@role_required('Instructor')
def instructor_index():
    coursesections = db.session.query(CourseSection).all()
    positions = db.session.query(Position).all()
    if current_user.user_type != 'Instructor':
        flash('You are not allowed to access Instructor Page')
        return redirect(url_for('auth.login'))
    return render_template('instructor_index.html', positions = positions, coursesections = coursesections)

