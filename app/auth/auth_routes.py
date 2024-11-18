from flask import render_template, flash, redirect, url_for, request
from app import db
from app.auth import auth_blueprint as bp_auth
import sqlalchemy as sqla
from app.main.models import User, Student, Instructor
from app.auth.auth_forms import LoginForm, StudentRegistrationForm, InstructorRegistrationForm
from flask_login import login_user, current_user, logout_user, login_required


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
        # for c in srform.Courses_taught.data:
        #     student.courses_taught.add(c)
        student.set_password(srform.password.data)
        db.session.add(student)
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
                flash('Invalid username or password')
                return redirect(url_for('auth.login'))
            login_user(user, remember=lform.remember_me.data)
            if current_user.user_type=='Student':
                return redirect(url_for('main.student_index'))
            else:
                return redirect(url_for('main.instructor_index'))

    return render_template('login.html', form = lform)

@bp_auth.route('/user/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))





