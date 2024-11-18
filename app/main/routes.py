from flask import render_template, flash, redirect, url_for, request, jsonify
import sqlalchemy as sqla
from app import db
from app.main import main_blueprint as bp_main
from flask_login import current_user, login_required
from app.decorators import role_required

@bp_main.route('/', methods=['GET'])
@bp_main.route('/index', methods=['GET'])
def index():
    return redirect(url_for('auth.login'))

@bp_main.route('/student_index', methods=['GET'])
@login_required
@role_required('Student')
def student_index():
    return render_template('student_index.html')

@bp_main.route('/instructor_index', methods=['GET'])
@login_required
@role_required('Instructor')
def instructor_index():
    return render_template('instructor_index.html')