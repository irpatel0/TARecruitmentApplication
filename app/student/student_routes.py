from flask import render_template, flash, redirect, url_for, request, jsonify
import sqlalchemy as sqla
from app import db
from app.student import student_blueprint as bp_student
from flask_login import current_user, login_required
from app.decorators import role_required
from app.student.student_forms import ApplyForm
from app.main.models import Course, Position, Instructor, CourseSection, Application

@bp_student.route("/positions/<position_id>/details", methods=["GET", "POST"])
@login_required
@role_required('Student')
def view_SA_details(position_id):
    thePosition = db.session.get(Position, position_id)
    courseSectionID = thePosition.section_id
    theCourseSection = db.session.get(CourseSection, courseSectionID)
    instructor = db.session.get(Instructor, theCourseSection.instructor_id)
    instructor_name = instructor.firstname + " " + instructor.lastname
    return jsonify({'num_SAs': thePosition.num_SAs, 'available': thePosition.available, 'min_GPA': thePosition.min_GPA, 'min_grade': thePosition.min_grade, 'date_posted': thePosition.timestamp, 'instructor' : instructor_name})

@bp_student.route('/positions/<position_id>/apply', methods=['GET', 'POST'])
@login_required
@role_required('Student')
def apply_course(position_id):
    aform = ApplyForm()
    course_position = sqla.select(Position).where(Position.id == position_id)
    check_applied = db.session.scalars(sqla.select(Application).where(Application.student_id == current_user.id, Application.position_id == position_id)).first()
    print(check_applied)
    if (check_applied is not None):
        flash('You have already applied for this course!')
        return redirect(url_for('main.index'))
    if aform.validate_on_submit():
        new_application = Application(
                            student_id = current_user.id,
                            position_id = position_id,
                            grade_aquired = aform.grade.data,
                            term_taken = aform.taken_term.data,
                            course_term = aform.course_term.data)
        db.session.add(new_application)
        db.session.commit()
        flash('You have successfully applied for the course!')
        return redirect(url_for('main.index'))
    return render_template('applycourse.html', form=aform, position=course_position)

@bp_student.route('/positions/<position_id>/withdraw', methods=['GET', 'POST'])
@login_required
@role_required('Student')
def withdraw_course(position_id):
    application = db.session.scalars(sqla.select(Application).where(Application.student_id == current_user.id, Application.position_id == position_id)).first()
    db.session.delete(application)
    db.session.commit()
    flash('You have successfully withdrawn your application.')
    return redirect(url_for('main.index'))


