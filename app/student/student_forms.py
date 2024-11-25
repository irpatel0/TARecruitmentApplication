# from flask_wtf import FlaskForm
# from app import db
# import sqlalchemy as sqla

from flask_wtf import FlaskForm
from wtforms.validators import  Length, DataRequired, Email, EqualTo, ValidationError
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField, IntegerField, FloatField, SelectMultipleField, SelectField
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField 
from wtforms.widgets import ListWidget, CheckboxInput
from app import db
import sqlalchemy as sqla
from wtforms.validators import  ValidationError, DataRequired, Length
from flask_login import current_user
from app.main.models import Course, CourseSection

class ApplyForm(FlaskForm):
    grade = SelectField('Grade earned in the course',choices = [(5, 'A'), (4, 'B'), (3, 'C'), (2, 'P'), (1, 'NR')], validators=[DataRequired()])
    taken_term = StringField('Year and Term you took the course (Ex. 2024B)', validators=[Length(min=1, max=5)])
    course_term = StringField('Year and Term you are applying for (Ex. 2024B)', validators=[Length(min=1, max=5)])
    submit = SubmitField('Apply')
