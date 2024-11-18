from flask import render_template, flash, redirect, url_for, request, jsonify
import sqlalchemy as sqla
from app import db
from app.instructor import instructor_blueprint as bp_instructor
from flask_login import current_user, login_required
from app.main.models import Course, Student, Instructor, CourseSection, Position


@bp_instructor.route('/instructor/createcourse', methods=['GET', 'POST'])
def create_course():
    return "Create Course"

@bp_instructor.route('/instructor/createposition', methods=['GET', 'POST'])
def create_position():
    return "Create Position"

@bp_instructor.route('/instructor/student', methods=['GET'])
def view_students():
    return "Student"

@bp_instructor.route('/instructor/student/<student_id>', methods=['GET'])
@login_required
def student_profile(student_id):
    student = db.session.get(Student, student_id)
    return render_template('student_profile.html', student = student)
    

@bp_instructor.route('/instructor/student/assign', methods=['GET', 'POST'])
def assign_student():
    return "Assign Student"
