from flask import render_template, flash, redirect, url_for, request, jsonify
import sqlalchemy as sqla
from app import db
from app.instructor import instructor_blueprint as bp_instructor
from flask_login import current_user, login_required
from app.main.models import Course, Student, Instructor, CourseSection, Position
from app.main.models import Course, Position
from app.main.forms import CourseForm, PositionForm


@bp_instructor.route('/instructor', methods=['GET'])
def index():
    return "CSASSIST-Instructor"

@bp_instructor.route('/instructor/create_course', methods=['GET'])
@login_required
def create_course():
    cform = CourseForm()
    if cform.validate_on_submit():
        new_course = Course(course_number = cform.course_number.data,
                            section = cform.section.data,
                            term = cform.term.data)
        db.session.add(new_course)
        db.session.commit()
        flash('The new course has successfully posted!')
        return redirect(url_for('main.index'))
    return render_template('createcourse.html', form=cform)

@bp_instructor.route('/instructor/create_position', methods=['GET', 'POST'])
@login_required
def create_position():
    pform = PositionForm()
    if pform.validate_on_submit():
        new_position = Position(
            section_id=pform.course_section.data.id,
            num_SAs=pform.num_SAs.data,
            min_GPA=pform.min_GPA.data,
            min_grade=pform.min_grade.data
        )
        db.session.add(new_position)
        db.session.commit()
        flash('The new position has been successfully added!')
        return redirect(url_for('main.index'))
    return render_template('createposition.html', form=pform)

@bp_instructor.route('/instructor/student', methods=['GET'])
def view_students():
    return "Student"

@bp_instructor.route('/instructor/student/<student_id>', methods=['GET'])
def student_profile(student_id):
    student = db.session.get(Student, student_id)
    return render_template('student_profile.html', student = student)


@bp_instructor.route('/instructor/student/assign', methods=['GET', 'POST'])
def assign_student():
    return "Assign Student"