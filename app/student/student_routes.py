from flask import render_template, flash, redirect, url_for, request, jsonify
import sqlalchemy as sqla
from app import db
from app.student import student_blueprint as bp_student
from flask_login import current_user, login_required
from app.decorators import role_required
from app.main.models import Course, Position, Instructor, CourseSection

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



