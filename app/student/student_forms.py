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
    taken_term = StringField('Term you took the course', validators=[Length(min=1, max=5), Regexp('^\d{4}[ABCDFS]$', message='Term should be a year followed by a term letter (Ex. 2024B).')])
    course_term = StringField('Term you are applying for', validators=[Length(min=1, max=5), Regexp('^\d{4}[ABCDFS]$', message='Term should be a year followed by a term letter (Ex. 2024B).')])
    submit = SubmitField('Apply')
