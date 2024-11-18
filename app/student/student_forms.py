from flask_wtf import FlaskForm
from wtforms.validators import  Length, DataRequired, Email, EqualTo, ValidationError
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField, IntegerField, FloatField
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField 
from wtforms.widgets import ListWidget, CheckboxInput
from app import db
import sqlalchemy as sqla
from app.main.models import Student

class StudentRegistrationForm(FlaskForm):
    
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    WPI_ID = StringField('WPI ID', validators=[DataRequired(), Length(min=9, max=10)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(10)])
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    GPA = FloatField('GPA', validators=[DataRequired()])
    # Courses_taught = QuerySelectMultipleField( 'Tag', query_factory= lambda : db.session.scalars(sqla.select(CourseSection)), get_label= lambda theCourse : theCourse.course_number, widget=ListWidget(prefix_label=False),
    #      option_widget=CheckboxInput() )
    graduation_date = StringField('Graduation Date', validators = [DataRequired()])
    submit = SubmitField('Register')


    def validate_wpi_id(self, WPI_ID):
        query = sqla.select(Student).where(Student.WPI_ID == WPI_ID.data)
        student = db.session.scalars(query).first()
        if student is not None:
            raise ValidationError('the WPI ID already exists!')

    def validate_email(self, email): #TO DO: MAKE SURE EMAIL IS A WPI EMAIL
        query = sqla.select(Student).where(Student.email == email.data)
        student = db.session.scalars(query).first()
        if student is not None:
            raise ValidationError('the email already exists!')
    
    def validate_phone(self, phone):
        query = sqla.select(Student).where(Student.phone == phone.data)
        student = db.session.scalars(query).first()
        if student is not None:
            raise ValidationError('the phone number already exists!')

    def validate_username(self, username):
        query = sqla.select(Student).where(Student.username == username.data)
        student = db.session.scalars(query).first()
        if student is not None:
            raise ValidationError('the username already exists!')

