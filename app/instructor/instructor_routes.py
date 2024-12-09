from flask import render_template, flash, redirect, url_for, request, jsonify
import sqlalchemy as sqla
from app import db
from app.instructor import instructor_blueprint as bp_instructor
from flask_login import current_user, login_required
from app.main.models import Course, Student, Instructor, CourseSection, Position
from app.instructor.instructor_forms import CourseForm, PositionForm, UpdateCourseForm
from app.decorators import role_required


@bp_instructor.route('/instructor', methods=['GET'])
@role_required('Instructor')
def index():
    return "CSASSIST-Instructor"

@bp_instructor.route('/instructor/create_course', methods=['GET', 'POST'])
@login_required
@role_required('Instructor')
def create_course():
    cform = CourseForm()
    if cform.validate_on_submit():
        print('inside validate')
        check_created = db.session.scalars(sqla.select(CourseSection).where(CourseSection.course_number == cform.course_number.data.number)
                                                                .where(CourseSection.section == cform.section.data)
                                                                .where(CourseSection.term == cform.term.data)
                                                                ).first()
        if (check_created is not None):
            flash('This course has already been created!')
            return redirect(url_for('main.index'))
        new_course = CourseSection(course_number = cform.course_number.data.number,
                            section = cform.section.data,
                            instructor_id = current_user.id,
                            term = cform.term.data)
        db.session.add(new_course)
        print('new course added')
        db.session.commit()
        course = db.session.scalars(sqla.select(CourseSection).where(CourseSection.course_number == 'CS1001')).first()
        #.where(
        #     CourseSection.instructor_id == 1)).first()
        print("****",course)
        flash('The new course has successfully posted!')
        return redirect(url_for('main.index'))
    return render_template('createcourse.html', form=cform)

@bp_instructor.route('/instructor/<section_id>/create_position', methods=['GET', 'POST'])
@login_required
@role_required('Instructor')
def create_position(section_id):
    pform = PositionForm()
    course_section = db.session.get(CourseSection, section_id)
    if pform.validate_on_submit():
        new_position = Position(
            section_id=section_id,
            num_SAs=pform.num_SAs.data,
            min_GPA=pform.min_GPA.data,
            min_grade=pform.min_grade.data
        )
        db.session.add(new_position)
        db.session.commit()
        flash('The new position has been successfully added!')
        return redirect(url_for('main.index'))
    return render_template('createposition.html', form=pform, section=course_section)

@bp_instructor.route('/instructor/student', methods=['GET'])
@role_required('Instructor')
def view_students():
    return "Student"

@bp_instructor.route('/instructor/student/<student_id>', methods=['GET'])
@role_required('Instructor')
def student_profile(student_id):
    student = db.session.get(Student, student_id)
    return render_template('student_profile.html', student = student)


@bp_instructor.route('/instructor/student/assign', methods=['GET', 'POST'])
@role_required('Instructor')
def assign_student():
    return "Assign Student"

@bp_instructor.route('/applications/<position_id>', methods=['GET', 'POST'])
@login_required
@role_required('Instructor')
def view_allstudents(position_id):
    applicants = db.session.get(Position, position_id)
    data = []
    for applicant in applicants.get_applications():
        student_name = applicant.get_student().firstname + " " + applicant.get_student().lastname
        availability = ""
        if applicant.get_only_student().assigned:
            availability = "Assigned"
        else:
            availability = "Unassigned"
        data.append({'student_id': applicant.student_id,
                     'student_name': student_name,
                     'grade_acquired': applicant.grade_aquired,
                     'term_taken': applicant.term_taken,
                     'course_term': applicant.course_term,
                     'status': applicant.status,
                     'availability': availability})

    return jsonify(data)

@bp_instructor.route('/coursesection/<cs_id>', methods=['GET', 'POST'])
@login_required
@role_required('Instructor')
def update_coursesection(cs_id):
    cs = db.session.get(CourseSection, cs_id)
    ucf = UpdateCourseForm()

    if request.method == 'POST':
        if ucf.validate_on_submit():
            cs.course_number = ucf.course_number.data.number
            cs.section = ucf.section.data
            cs.term = ucf.term.data
            db.session.commit()
            flash('Your course section has been updated')
            return redirect(url_for('main.instructor_index'))
    elif request.method == 'GET':
        ucf.course_number.data = cs.course
        ucf.section.data = cs.section
        ucf.term.data = cs.term
    else:
        pass
    return render_template('update_course_section.html', form=ucf)


