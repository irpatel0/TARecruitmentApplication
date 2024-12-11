# from flask_wtf import FlaskForm
# from app import db
# import sqlalchemy as sqla

from flask_wtf import FlaskForm
from wtforms.validators import  Length, DataRequired, Email, EqualTo, ValidationError, Regexp
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField, IntegerField, FloatField, SelectMultipleField, SelectField
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField 
from wtforms.widgets import ListWidget, CheckboxInput
from app import db
import sqlalchemy as sqla
from wtforms.validators import  ValidationError, DataRequired, Length
from flask_login import current_user
from app.main.models import Course, CourseSection

class ApplyForm(FlaskForm):
    grade = SelectField('Grade earned in the course',choices = [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('F', 'F'), ('NR', 'NR')], validators=[DataRequired()])
    year_taken = StringField('Year you took the course', validators=[Length(min=1, max=4), Regexp('^\d{4}$', message='Please enter a valid 4-digit year')])
    term_taken = SelectField('Term you took the course',choices = [('A', 'A-Term'), ('B', 'B-Term'), ('C', 'C-Term'), ('D', 'D-Term'), ('F', 'Fall Semester'), ('S', 'Spring Semester')], validators=[DataRequired()])
    submit = SubmitField('Apply')
