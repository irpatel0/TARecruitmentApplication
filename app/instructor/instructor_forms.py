# from flask_wtf import FlaskForm
# from app import db
# import sqlalchemy as sqla

from flask_wtf import FlaskForm
from wtforms.validators import  Length, DataRequired, Email, EqualTo, ValidationError
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField, IntegerField, FloatField, SelectMultipleField
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField 
from wtforms.widgets import ListWidget, CheckboxInput
from app import db
import sqlalchemy as sqla
from wtforms.validators import  ValidationError, DataRequired, Length
from flask_login import current_user
from app.main.models import Course, CourseSection

class CourseForm(FlaskForm):
    course_number = QuerySelectField('Course Number',
                query_factory = lambda: db.session.scalars(sqla.select(Course).order_by(sqla.text('Course.number'))),
                get_label = lambda theCourse : f"{theCourse.number} - {theCourse.title}"
    )
    section =  StringField('Section', validators=[Length(min=1, max=5)])
    term = StringField('Term', validators=[Length(min=1, max=5)])
    submit = SubmitField('Post')

class PositionForm(FlaskForm):
    course_section = QuerySelectField('Course Section',
                query_factory = lambda: db.session.scalars(sqla.select(CourseSection).where(CourseSection.instructor_id == current_user.id)),
                get_label = lambda theCourseSection : f"{theCourseSection.course_number}-{theCourseSection.section} ({theCourseSection.term})"
    )
    num_SAs = IntegerField('Number of SAs', validators=[DataRequired()])
    min_GPA = FloatField('Min GPA', validators=[DataRequired()])
    min_grade = StringField('Min Grade', validators=[DataRequired(), Length(max=2)])
    submit = SubmitField('Post')