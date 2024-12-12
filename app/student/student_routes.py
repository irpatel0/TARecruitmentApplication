from flask import render_template, flash, redirect, url_for, request, jsonify
import sqlalchemy as sqla
from app import db
from app.student import student_blueprint as bp_student
from flask_login import current_user, login_required
from app.decorators import role_required
from app.student.student_forms import ApplyForm
from app.main.models import Course, Position, Instructor, CourseSection, Application, CourseTaken

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

    
    course_position = db.session.get(Position, position_id)
    course_section_ID = course_position.section_id
    course_section = db.session.get(CourseSection, course_section_ID)
    course = db.session.scalars(sqla.select(Course).where(Course.number == course_section.course_number)).first()
    check_applied = db.session.scalars(sqla.select(Application).where(Application.student_id == current_user.id, Application.position_id == position_id)).first()
    check_accepted = db.session.scalars(sqla.select(Application).where(Application.student_id == current_user.id, Application.status == 'Approved')).first()
    check_taken = db.session.scalars(sqla.select(CourseTaken).where(CourseTaken.student_id == current_user.id)
                                                                .where(CourseTaken.course_id == course.id)).first()
    if (check_applied is not None):
        flash('You have already applied for this course!')
        return redirect(url_for('main.index'))
    if (check_accepted is not None):
        flash('You have already been accepted to a course!')
        return redirect(url_for('main.index'))
    if (course_position.num_Assigned >= course_position.num_SAs):
        flash('This course is already full!')
        return redirect(url_for('main.index'))
    taught_course = False
    if course in current_user.get_taught():
        taught_course = True
    else:
        taught_course = False
    if (check_taken is not None):
        aform = ApplyForm(grade = check_taken.grade)
    else:
        aform = ApplyForm()
    if aform.validate_on_submit():
        new_application = Application(
                            student_id = current_user.id,
                            position_id = position_id,
                            grade_aquired = aform.grade.data,
                            term_taken = aform.year_taken.data + aform.term_taken.data)

        if (check_taken is None):
            new_course_taken = CourseTaken(
                                student_id = current_user.id,
                                course_id = course.id,
                                grade = aform.grade.data)
            db.session.add(new_course_taken)
        else:
            check_taken.grade = aform.grade.data
    
        db.session.add(new_application)
        db.session.commit()
        flash('You have successfully applied for the course!')
        return redirect(url_for('main.index'))
    if check_taken is None:
        return render_template('applycourse.html', form=aform, position=course_position, section = course_section, taken = False, taught = taught_course)
    else:
        return render_template('applycourse.html', form=aform, position=course_position, section = course_section, taken = check_taken, taught = taught_course)

@bp_student.route('/positions/<position_id>/withdraw', methods=['GET', 'POST'])
@login_required
@role_required('Student')
def withdraw_course(position_id):
    application = db.session.scalars(sqla.select(Application).where(Application.student_id == current_user.id, Application.position_id == position_id)).first()
    db.session.delete(application)
    db.session.commit()
    flash('You have successfully withdrawn your application.')
    return redirect(url_for('main.index'))


