from flask import render_template, flash, redirect, url_for, request
from app import db
from app.auth import auth_blueprint as bp_auth
from app.student import student_blueprint as bp_student
from app.instructor import instructor_blueprint as bp_instructor
from app.student.student_forms import StudentRegistrationForm
from app.instructor.instructor_forms import InstructorRegistrationForm
from flask_login import current_user, login_required #login_user, current_user, logout_user, login_required
import sqlalchemy as sqla
from app.main.models import Student, Instructor


@bp_student.route('/student/studentregister', methods=['POST'])
def student_register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    srform = StudentRegistrationForm()
    if srform.validate_on_submit():
        student = Student( username = srform.username.data,
                           firstname = srform.first_name.data,
                           lastname = srform.last_name.data,
                           wpi_id = srform.WPI_ID.data,
                           email = srform.email.data,
                           phone = srform.phone.data,
                           gpa = srform.GPA.data,
                           graduation_date = srform.graduation_date.data,
                           )
        for c in srform.Courses_taught.data:
            student.courses_taught.add(c)
        student.set_password(srform.password.data)
        db.session.add(student)
        db.session.commit()
        flash('Congratulations, you are now a registered student user!')
        return redirect_url(url_for('main.index'))
    
    return render_template('student_register.html', form = srform)



@bp_instructor.route('/instructor/register', methods=['POST'])
def instructor_register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    irform = InstructorRegistrationForm()
    if irform.validate_on_submit():
        instructor = Instructor( username = irform.username.data,
                           firstname = irform.first_name.data,
                           lastname = irform.last_name.data,
                           wpi_id = irform.WPI_ID.data,
                           email = irform.email.data,
                           phone = irform.phone.data,
                           )
        instructor.set_password(irform.password.data)
        db.session.add(instructor)
        db.session.commit()
        flash('Congratulations, you are now a registered instructor user!')
        return redirect_url(url_for('main.index'))
    
    return render_template('instructor_register.html', form = irform)


