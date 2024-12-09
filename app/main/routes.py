from flask import render_template, flash, redirect, url_for, request, jsonify
import sqlalchemy as sqla
from app import db
from app.main import main_blueprint as bp_main
from flask_login import current_user, login_required
from app.decorators import role_required
from app.main.models import Course, Position,  CourseSection
from app.main.forms import StudentEditForm, InstructorEditForm


@bp_main.route('/', methods=['GET'])
@bp_main.route('/index', methods=['GET'])
@login_required
def index():
    return redirect(url_for('auth.login'))

@bp_main.route('/student_index', methods=['GET'])
@login_required
@role_required('Student')
def student_index():
    positions = db.session.scalars(sqla.select(Position).order_by(Position.timestamp.desc())).all()
    applied_positions = {position.id for position in positions if current_user.applied_to(position.id)}
    recommended_positions = sorted(positions, key=lambda position: position.recommendation_score(current_user), reverse=True)

    return render_template('student_index.html', positions = positions, applied=applied_positions, recommended = recommended_positions)

@bp_main.route('/instructor_index', methods=['GET'])
@login_required
@role_required('Instructor')
def instructor_index():
    coursesections = db.session.query(CourseSection).where(CourseSection.instructor_id == current_user.id).all()
    positions = db.session.query(Position).all()
    return render_template('instructor_index.html', positions = positions, coursesections = coursesections)

@bp_main.route('/user/student/editprofile', methods=['GET', 'POST'])
@login_required
@role_required('Student')
def student_edit_profile():
    eform = StudentEditForm()
    if request.method == 'POST':
        if eform.validate_on_submit():
            current_user.firstname = eform.first_name.data
            current_user.lastname = eform.last_name.data
            current_user.wpi_id = eform.wpi_id.data
            current_user.email = eform.email.data
            current_user.phone = eform.phone.data
            current_user.set_password(eform.password.data)
            current_user.gpa = eform.GPA.data
            current_user.graduation_date = eform.graduation_date.data
            for t in current_user.get_taught():
                current_user.taught.remove(t)
            for t in eform.courses_taught.data:
                current_user.taught.add(t)
            db.session.add(current_user)
            db.session.commit()
            flash('Your profile has been updated')
            return redirect(url_for('main.index'))
    elif request.method == 'GET':
        eform.first_name.data = current_user.firstname
        eform.last_name.data = current_user.lastname
        eform.wpi_id.data = current_user.wpi_id
        eform.email.data = current_user.email
        eform.phone.data = current_user.phone
        eform.GPA.data = current_user.gpa
        eform.graduation_date.data = current_user.graduation_date
        for t in current_user.get_taught():
            eform.courses_taught.data.append(t)
    else:
        pass
    return render_template('student_edit_profile.html', eform=eform)

@bp_main.route('/user/instructor/editprofile', methods=['GET', 'POST'])
@login_required
@role_required('Instructor')
def instructor_edit_profile():
    eform = InstructorEditForm()
    if request.method == 'POST':
        if eform.validate_on_submit():
            current_user.firstname = eform.first_name.data
            current_user.lastname = eform.last_name.data
            current_user.wpi_id = eform.wpi_id.data
            current_user.email = eform.email.data
            current_user.phone = eform.phone.data
            current_user.set_password(eform.password.data)
            db.session.add(current_user)
            db.session.commit()
            flash('Your profile has been updated')
            return redirect(url_for('main.index'))
    elif request.method == 'GET':
        eform.first_name.data = current_user.firstname
        eform.last_name.data = current_user.lastname
        eform.wpi_id.data = current_user.wpi_id
        eform.email.data = current_user.email
        eform.phone.data = current_user.phone
    else:
        pass
    return render_template('instructor_edit_profile.html', eform=eform)
