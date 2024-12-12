from flask import render_template, flash, redirect, url_for, request, jsonify
import sqlalchemy as sqla
from app import db
from app.instructor import instructor_blueprint as bp_instructor
from flask_login import current_user, login_required
from app.main.models import Course, Student, Instructor, CourseSection, Position, Application
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
    print('route called')
    cform = CourseForm()
    if cform.validate_on_submit():
        print('inside validate')
        check_created = db.session.scalars(sqla.select(CourseSection).where(CourseSection.course_number == cform.course_number.data.number)
                                                                .where(CourseSection.section == cform.section.data)
                                                                .where(CourseSection.term == cform.year.data + cform.term.data)
                                                                ).first()
        if (check_created is not None):
            flash('This course has already been created!')
            return redirect(url_for('main.index'))
        new_course = CourseSection(course_number = cform.course_number.data.number,
                            section = cform.section.data,
                            instructor_id = current_user.id,
                            term = cform.year.data + cform.term.data)
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


# @bp_instructor.route('/instructor/student/assign', methods=['GET', 'POST'])
# @role_required('Instructor')
# def assign_student():
#     return "Assign Student"

@bp_instructor.route('/applications/<position_id>', methods=['GET', 'POST'])
@login_required
@role_required('Instructor')
def view_allstudents(position_id):
    applicants = db.session.get(Position, position_id)
    data = []
    for applicant in applicants.get_applications():
        student_name = applicant.get_student().firstname + " " + applicant.get_student().lastname
        student = db.session.get(Student, applicant.get_student().id)
        applications = db.session.scalars(sqla.select(Application)).all() #.where(Application.applicant.id == student.id)).first() 
        approved_application = 0 
        availability = "Unassigned"
        for application in applications:
            if application.applicant.id == student.id:
                approved_application = application
        section_id = applicants.section_id
        course_section = db.session.get(CourseSection, section_id)

        student_allterms = db.session.scalars(student.assigned_terms.select()).all()
        student_coursesection_id = 0; 
        for term in student_allterms:
            if course_section.term == term.term:
                student_coursesection_id = course_section.id
        student_coursesection = db.session.get(CourseSection, student_coursesection_id)
        if student_coursesection is not None: 
            if course_section.term == student_coursesection.term:
                availability = "Assigned"
            # else:
            #     availability = "Unassigned"


        #availability = ""
        # if applicant.get_only_student().assigned:
        #     availability = "Assigned"
        # else:
        #     availability = "Unassigned"
        data.append({'student_id': applicant.student_id,
                     'student_name': student_name,
                     'grade_acquired': applicant.grade_aquired,
                     'term_taken': applicant.term_taken,
                     'status': applicant.status,
                     'availability': availability,
                     'grade_point_average': student.gpa})

    return jsonify(data)

@bp_instructor.route('/coursesection/<cs_id>/update', methods=['GET', 'POST'])
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

@bp_instructor.route('/coursesection/<cs_id>/delete', methods=['GET', 'POST'])
@login_required
@role_required('Instructor')
def delete_coursesection(cs_id):
    cs = db.session.get(CourseSection, cs_id)
    if cs:
        for student in db.session.scalars(cs.assigned_students.select()):
            cs.assigned_students.remove(student)
            db.session.commit()
        pos = db.session.scalars(sqla.select(Position).where(Position.section_id == cs_id)).first()
        if pos:
            applications = db.session.scalars(sqla.select(Application).where(Application.position_id == pos.id)).all()
            if applications:
                for application in applications:
                    db.session.delete(application)
                    db.session.commit()
            db.session.delete(pos)
            db.session.commit()
        db.session.delete(cs)
        db.session.commit()
        flash('Your course section has been deleted')
    return redirect(url_for('main.instructor_index'))


@bp_instructor.route('/position/<position_id>/student/<student_id>/accept', methods=['GET', 'POST'])
@login_required
@role_required('Instructor')
def accept_student(position_id, student_id):

    position = db.session.get(Position, position_id)
    student = db.session.get(Student, student_id)
    applications = db.session.scalars(sqla.select(Application)).all() #.where(Application.applicant.id == student.id)).first() 
    approved_application = 0 
    for application in applications:
        if application.applied_to.id == position.id and application.applicant.id == student.id:
            approved_application = application
    section_id = position.section_id
    course_section = db.session.get(CourseSection, section_id)

    if (position.num_Assigned < position.num_SAs):
        student_allterms = db.session.scalars(student.assigned_terms.select()).all()
        #print(student_allterms)
        student_coursesection_id = 0; 
        for term in student_allterms:
            if course_section.term == term.term:
                student_coursesection_id = course_section.id
        #print(student_coursesection_id)
        student_coursesection = db.session.get(CourseSection, student_coursesection_id)
        #print(student_coursesection)
        if student_coursesection is not None: 
            #print('hi' + course_section.term, student_coursesection.term)
            if course_section.term == student_coursesection.term:
                flash("Student has already been assigned an SA position in this term")
                return(redirect(url_for('main.instructor_index')))
        position.num_Assigned = position.num_Assigned + 1
        approved_application.status = 'Approved'
        student.assigned_terms.add(course_section)
        if position.num_Assigned == position.num_SAs - 1:
            position.available == False; 
        #### ADDING TO PAST ENROLLMENTS
        student.taught.add(course_section.course)
        ######
        db.session.commit()
        flash('Student successfully assigned to SA position')
        return(redirect(url_for('main.instructor_index')))
    else:
        flash('This course already has maximum number of SAs!')
        return(redirect(url_for('main.instructor_index')))


@bp_instructor.route('/position/<position_id>/student/<student_id>/reject', methods=['GET', 'POST'])
@login_required
@role_required('Instructor')
def reject_student(position_id, student_id):
    
    student = db.session.get(Student, student_id)
    position = db.session.get(Position, position_id)
    #student_applications = db.session.scalars(student.student_applications.select()).all()
    applications = db.session.scalars(sqla.select(Application)).all() #.where(Application.applicant.id == student.id)).first() 

    rejected_application = 0
    print(applications)
    for application in applications:
        if application.applicant.id == student.id:
            if application.position_id == position.id:
                rejected_application = application
                print(rejected_application)
                rejected_application.status = 'Rejected'
                db.session.commit()
                flash('Student application status updated to rejected')
                return (redirect(url_for('main.instructor_index')))
            

@bp_instructor.route('/instructor/closedpositions', methods=['GET', 'POST'])
@login_required
@role_required('Instructor')
def view_closedpositions():
    coursesections = db.session.query(CourseSection).where(CourseSection.instructor_id == current_user.id).all()
    positions = db.session.query(Position).all()
    return render_template('closedpositions.html', positions = positions, coursesections = coursesections)




