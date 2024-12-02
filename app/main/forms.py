from flask_wtf import FlaskForm
from app import db
import sqlalchemy as sqla
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError, Regexp, NumberRange
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField, IntegerField, FloatField, SelectMultipleField
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from app.main.models import Student, User, Course
from flask_login import current_user

class StudentEditForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    wpi_id = StringField('WPI ID', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    GPA = FloatField('GPA', validators=[DataRequired(message="Enter a valid GPA between 0 and 4.00"), NumberRange(0, 4)])
    courses_taught = QuerySelectMultipleField('Courses Taught',
                                              query_factory=lambda: db.session.scalars(
                                                  sqla.select(Course).order_by(Course.number)),
                                              get_label=lambda theCourse: f"{theCourse.number} - {theCourse.title}",
                                              widget=ListWidget(prefix_label=False),
                                              option_widget=CheckboxInput()
                                              )
    graduation_date = StringField('Graduation Date', validators=[DataRequired()])
    submit = SubmitField('Update Profile')

    def validate_wpi_id(self, wpi_id):
        if not str(wpi_id.data).isnumeric():
            raise ValidationError('Please enter valid WPI ID with all numeric digits')
        if len(str(wpi_id.data)) != 9:
            raise ValidationError('Please enter valid WPI ID of 9 digits')
        query = sqla.select(User).where(User.wpi_id == wpi_id.data)
        student = db.session.scalars(query).first()
        if student is not None:
            if student.id != current_user.id:
                raise ValidationError('the WPI ID already exists!')

    def validate_email(self, email):  # TO DO: MAKE SURE EMAIL IS A WPI EMAIL
        query = sqla.select(User).where(User.email == email.data)
        student = db.session.scalars(query).first()
        if student is not None:
            if student.id != current_user.id:
                raise ValidationError('the email already exists!')
        if "wpi.edu" not in email.data:
            raise ValidationError('Please enter valid WPI email address')

    def validate_phone(self, phone):
        if not str(phone.data).isnumeric():
            raise ValidationError('Please enter valid phone number with all numeric digits')
        if len(str(phone.data)) != 10:
            raise ValidationError('Please enter valid phone number of 10 digits')
        query = sqla.select(User).where(User.phone == phone.data)
        student = db.session.scalars(query).first()
        if student is not None:
            if student.id != current_user.id:
                raise ValidationError('the phone number already exists!')

    def validate_graduation_date(self, graduation_date):
        if not str(graduation_date.data).isnumeric():
            raise ValidationError('Please enter valid graduation date with all numeric digits')
        if len(str(graduation_date.data)) != 4:
            raise ValidationError('Please enter valid graduation date with 4 digit year')

class InstructorEditForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    wpi_id = StringField('WPI ID', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update Profile')

    def validate_wpi_id(self, wpi_id):
        if not str(wpi_id.data).isnumeric():
            raise ValidationError('Please enter valid WPI ID with all numeric digits')
        if len(str(wpi_id.data)) != 9:
            raise ValidationError('Please enter valid WPI ID of 9 digits')
        query = sqla.select(User).where(User.wpi_id == wpi_id.data)
        instructor = db.session.scalars(query).first()
        if instructor is not None:
            if instructor.id != current_user.id:
                raise ValidationError('the WPI ID already exists!')

    def validate_email(self, email):  # TO DO: MAKE SURE EMAIL IS A WPI EMAIL
        query = sqla.select(User).where(User.email == email.data)
        instructor = db.session.scalars(query).first()
        if instructor is not None:
            if instructor.id != current_user.id:
                raise ValidationError('the email already exists!')
        if "wpi.edu" not in email.data:
            raise ValidationError('Please enter valid WPI email address')

    def validate_phone(self, phone):
        if not str(phone.data).isnumeric():
            raise ValidationError('Please enter valid phone number with all numeric digits')
        if len(str(phone.data)) != 10:
            raise ValidationError('Please enter valid phone number of 10 digits')
        query = sqla.select(User).where(User.phone == phone.data)
        instructor = db.session.scalars(query).first()
        if instructor is not None:
            if instructor.id != current_user.id:
                raise ValidationError('the phone number already exists!')
