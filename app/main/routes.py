from flask import render_template, flash, redirect, url_for, request, jsonify
import sqlalchemy as sqla
from app import db
from app.main import main_blueprint as bp_main
from flask_login import current_user, login_required
from app.decorators import role_required
from app.main.models import Course, Position,  CourseSection


@bp_main.route('/', methods=['GET'])
@bp_main.route('/index', methods=['GET'])
@login_required
def index():
    return redirect(url_for('auth.login'))

@bp_main.route('/student_index', methods=['GET'])
@login_required
@role_required('Student')
def student_index():
    positions = db.session.scalars(sqla.select(Position)).all()
    return render_template('student_index.html', positions = positions)

@bp_main.route('/instructor_index', methods=['GET'])
@login_required
@role_required('Instructor')
def instructor_index():
    coursesections = db.session.query(CourseSection).where(CourseSection.instructor_id == current_user.id).all()
    positions = db.session.query(Position).all()
    return render_template('instructor_index.html', positions = positions, coursesections = coursesections)

