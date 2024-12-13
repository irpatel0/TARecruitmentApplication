from flask import render_template, flash, redirect, url_for, request, Flask, session
from app import db
from app.auth import auth_blueprint as bp_auth
import sqlalchemy as sqla
from app.main.models import User, Student, Instructor, Course, CourseTaken
from app.auth.auth_forms import LoginForm, StudentRegistrationForm, InstructorRegistrationForm, SSO_StudentRegistrationForm, SSO_InstructorRegistrationForm
from flask_login import login_user, current_user, logout_user, login_required
import identity.web
import requests
from flask_session import Session
from app.decorators import session_required
from config import Config as appconfig

ssoauth = identity.web.Auth(
    session=session,
    authority=appconfig.AUTHORITY,
    client_id=appconfig.CLIENT_ID,
    client_credential=appconfig.CLIENT_SECRET
)

@bp_auth.route('/student/studentregister', methods=['GET', 'POST'])
def student_register():
    if current_user.is_authenticated:
        return redirect(url_for('main.student_index'))

    srform = StudentRegistrationForm()
    if srform.validate_on_submit():
        student = Student(username=srform.username.data,
                          firstname=srform.first_name.data,
                          lastname=srform.last_name.data,
                          wpi_id=srform.wpi_id.data,
                          email=srform.email.data,
                          phone=srform.phone.data,
                          gpa=srform.GPA.data,
                          graduation_date=srform.graduation_date.data,
                          )

        courses = [
            {
                "course_name": course_form.course.data.title,
                "grade": course_form.grade.data,
                "sa_experience": course_form.sa_experience.data,
            }
            for course_form in srform.courses
        ]

        student.set_password(srform.password.data)
        db.session.add(student)
        db.session.commit()
        for course in courses:
            course_obj = db.session.scalars(sqla.select(Course).where(Course.title == course['course_name'])).first()
            course_taken = CourseTaken(student_id=student.id, course_id=course_obj.id, grade=course['grade'])
            db.session.add(course_taken)
            if(course['sa_experience'] == True):
                student.taught.add(course_obj)
            db.session.commit()
        flash('Congratulations, you are now a registered student user!')
        return redirect(url_for('main.index'))
    return render_template('student_register.html', form=srform)


@bp_auth.route('/instructor/register', methods=['GET', 'POST'])
def instructor_register():
    if current_user.is_authenticated:
        return redirect(url_for('main.instructor_index'))

    irform = InstructorRegistrationForm()
    if irform.validate_on_submit():
        instructor = Instructor(username=irform.username.data,
                                firstname=irform.first_name.data,
                                lastname=irform.last_name.data,
                                wpi_id=irform.wpi_id.data,
                                email=irform.email.data,
                                phone=irform.phone.data,
                                )
        instructor.set_password(irform.password.data)
        db.session.add(instructor)
        db.session.commit()
        flash('Congratulations, you are now a registered instructor user!')
        return redirect(url_for('main.index'))

    return render_template('instructor_register.html', form=irform)

@bp_auth.route('/user/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.user_type == 'Student':
            return redirect(url_for('main.student_index'))
        else:
            return redirect(url_for('main.instructor_index'))

    lform = LoginForm()

    if request.method == 'POST':
        if lform.validate_on_submit():
            query = sqla.select(User).where(User.username == lform.username.data)
            user = db.session.scalars(query).first()

            if (user is None) or(user.get_password(lform.password.data) == False):
                flash('Invalid username or password!')
                return redirect(url_for('auth.login'))
            login_user(user, remember=lform.remember_me.data)
            if current_user.user_type=='Student':
                return redirect(url_for('main.student_index'))
            else:
                return redirect(url_for('main.instructor_index'))

    return render_template('login.html', form = lform)

@bp_auth.route(appconfig.REDIRECT_PATH)
def auth_response():
    result = ssoauth.complete_log_in(request.args)
    if "error" in result:
        return render_template("sso_error.html", result=result)
    session['name'] = ssoauth.get_user()['name'] # useful while registering initially, when collected other info and user type
    session['email'] = ssoauth.get_user()['preferred_username']
    username = ssoauth.get_user()['preferred_username'].split('@')[0]
    checkuser = db.session.scalars(sqla.select(User).where(User.username == username)).first()
    if checkuser is None: # create page to gather data and user type, register in db
        return render_template("sso_choose_user.html", name=ssoauth.get_user()['name'])
    else:
        login_user(checkuser, remember=False)
        return redirect(url_for('auth.login'))


@bp_auth.route('/user/login/sso')
def login_sso():
    return render_template('login_sso.html', **ssoauth.log_in(
        scopes=appconfig.SCOPE, # Have user consent to scopes during log-in
        redirect_uri=url_for("auth.auth_response", _external=True), # Optional. If present, this absolute URL must match your app's redirect_uri registered in Microsoft Entra admin center
        prompt="select_account",  # Optional.
        ))


@bp_auth.route('/user/instructor/register/sso', methods=["GET", "POST"])
@session_required(session)
def instructor_register_sso():
    if current_user.is_authenticated:
        return redirect(url_for('main.instructor_index'))

    irform = SSO_InstructorRegistrationForm()
    if request.method == "POST":
        if irform.validate_on_submit():
            lname, fname = session['name'].split(',')
            instructor = Instructor(username = session['email'].split('@')[0],
                                    firstname=fname.strip(),
                                    lastname=lname.strip(),
                                    wpi_id=irform.wpi_id.data,
                                    email=session['email'],
                                    phone=irform.phone.data,
                                    )
            db.session.add(instructor)
            db.session.commit()
            user = db.session.scalars(sqla.select(User).where(User.username == session['email'].split('@')[0])).first()
            login_user(user, remember=False)
            flash('Congratulations, you are now a registered instructor and logged in with WPI SSO!')
            return redirect(url_for('main.instructor_index'))

    return render_template("instructor_register_sso.html", form=irform, name=session['name'])


@bp_auth.route('/user/student/register/sso', methods=["GET", "POST"])
@session_required(session)
def student_register_sso():
    if current_user.is_authenticated:
        return redirect(url_for('main.student_index'))

    srform = SSO_StudentRegistrationForm()
    if request.method == "POST":
        if srform.validate_on_submit():
            lname, fname = session['name'].split(',')
            student = Student(username=session['email'].split('@')[0],
                              firstname=fname.strip(),
                              lastname=lname.strip(),
                              wpi_id=srform.wpi_id.data,
                              email=session['email'],
                              phone=srform.phone.data,
                              gpa=srform.GPA.data,
                              graduation_date=srform.graduation_date.data,
                              )
            courses = [
                {
                    "course_name": course_form.course.data.title,
                    "grade": course_form.grade.data,
                    "sa_experience": course_form.sa_experience.data,
                }
                for course_form in srform.courses
            ]

            db.session.add(student)
            db.session.commit()

            for course in courses:
                course_obj = db.session.scalars(
                    sqla.select(Course).where(Course.title == course['course_name'])).first()
                course_taken = CourseTaken(student_id=student.id, course_id=course_obj.id, grade=course['grade'])
                db.session.add(course_taken)
                db.session.commit()
                if (course['sa_experience'] == True):
                    student.taught.add(course_obj)

            user = db.session.scalars(sqla.select(User).where(User.username == session['email'].split('@')[0])).first()
            login_user(user, remember=False)
            flash('Congratulations, you are now a registered student and logged in with WPI SSO!!')
            return redirect(url_for('main.student_index'))

    return render_template("student_register_sso.html", form=srform, name=session['name'])


@bp_auth.route('/user/logout', methods=['GET'])
@login_required
def logout():
    session.clear()
    ssoauth.log_out(url_for("main.index", _external=True))
    logout_user()
    return redirect(url_for('auth.login'))






