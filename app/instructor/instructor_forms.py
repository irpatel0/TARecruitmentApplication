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
from wtforms import StringField, SubmitField, SelectField, TextAreaField, BooleanField, IntegerField, FloatField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import  ValidationError, DataRequired, Length
from app.main.models import Course, CourseSection

class CourseForm(FlaskForm):
    course_number = QuerySelectField('Course Number',
                query_factory = lambda: db.session.scalars(sqla.select(Course).order_by(sqla.text('Course.number'))),
                get_label = lambda theCourse : theCourse.number
    )
    section =  StringField('Section', validators=[Length(min=1, max=5)])
    term = StringField('Term', validators=[Length(min=1, max=5)])
    submit = SubmitField('Post')

class PositionForm(FlaskForm):
    num_SAs = IntegerField('Number of SAs', validators=[DataRequired()])
    min_GPA = FloatField('Min GPA', validators=[DataRequired()])
    min_grade = StringField('Min Grade', validators=[DataRequired(), Length(max=1)])
    submit = SubmitField('Post')