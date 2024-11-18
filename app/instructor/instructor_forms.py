# from flask_wtf import FlaskForm
# from app import db
# import sqlalchemy as sqla

from flask_wtf import FlaskForm
from wtforms.validators import  Length, DataRequired, Email, EqualTo, ValidationError
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField, IntegerField, FloatField
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField 
from wtforms.widgets import ListWidget, CheckboxInput
from app import db
import sqlalchemy as sqla
from app.main.models import Instructor



class InstructorRegistrationForm(FlaskForm):
    
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    WPI_ID = IntegerField('WPI ID', validators=[DataRequired(), Length(min=9, max=9)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = IntegerField('Phone Number', validators=[DataRequired(), Length(min=10, max=10)])
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


    def validate_WPI_id(self, WPI_ID):
        query = sqla.select(Instructor).where(Instructor.WPI_ID == WPI_ID.data)
        instructor = db.session.scalars(query).first()
        if instructor is not None:
            raise ValidationError('the WPI ID already exists!')

    def validate_email(self, email): #TO DO: MAKE SURE EMAIL IS A WPI EMAIL
        query = sqla.select(Instructor).where(Instructor.email == email.data)
        instructor = db.session.scalars(query).first()
        if instructor is not None:
            raise ValidationError('the email already exists!')
    
    def validate_phone(self, phone):
        query = sqla.select(Instructor).where(Instructor.phone == phone.data)
        instructor = db.session.scalars(query).first()
        if instructor is not None:
            raise ValidationError('the phone number already exists!')

    def validate_username(self, username):
        query = sqla.select(Instructor).where(Instructor.username == username.data)
        instructor = db.session.scalars(query).first()
        if instructor is not None:
            raise ValidationError('the username already exists!')