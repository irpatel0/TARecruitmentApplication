from flask import render_template, flash, redirect, url_for, request, jsonify
import sqlalchemy as sqla
from app import db
from app.instructor import instructor_blueprint as bp_instructor

@bp_instructor.route('/instructor', methods=['GET'])
def index():
    return "CSASSIST-Instructor"

@bp_instructor.route('/instructor/createcourse', methods=['GET', 'POST'])
def create_course():
    return "Create Course"

@bp_instructor.route('instructor/createposition', methods=['GET', 'POST'])
def create_position():
    return "Create Position"

@bp_instructor.route('/instructor/student', methods=['GET'])
def student():
    return "Student"

@bp_instructor.route('/instructor/student/<student_id>', methods=['GET'])
def student_profile(student_id):
    return "Student Profile"


@bp_instructor.route('/instructor/student/assign', methods=['GET', 'POST'])
def assign_student():
    return "Assign Student"
