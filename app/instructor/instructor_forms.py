# from flask_wtf import FlaskForm
# from app import db
# import sqlalchemy as sqla

from flask_wtf import FlaskForm
from wtforms.validators import  Length, DataRequired, Email, EqualTo, ValidationError, NumberRange, Regexp
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField, IntegerField, FloatField, SelectField
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
    year = StringField('Year the course is being taught', validators=[Length(min=1, max=4), Regexp('^\d{4}$', message='Please enter a valid 4-digit year')])
    term = SelectField('Term the course is being taught',choices = [('A', 'A-Term'), ('B', 'B-Term'), ('C', 'C-Term'), ('D', 'D-Term'), ('F', 'Fall Semester'), ('S', 'Spring Semester')], validators=[DataRequired()])
    submit = SubmitField('Post')

class PositionForm(FlaskForm):
    # course_section = QuerySelectField('Course Section',
    #             query_factory = lambda: db.session.scalars(sqla.select(CourseSection).where(CourseSection.instructor_id == current_user.id)),
    #             get_label = lambda theCourseSection : f"{theCourseSection.course_number}-{theCourseSection.section} ({theCourseSection.term})"
    # )
    num_SAs = IntegerField('Number of SAs', validators=[DataRequired(), NumberRange(min=0)])
    min_GPA = FloatField('Min GPA', validators=[DataRequired(), NumberRange(0, 4)])
    min_grade = SelectField('Min Grade', choices = [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('F', 'F'), ('NR', 'NR')], validators=[DataRequired()])
    submit = SubmitField('Post')

class UpdateCourseForm(FlaskForm):
    course_number = QuerySelectField('Course Number',
                query_factory = lambda: db.session.scalars(sqla.select(Course).order_by(sqla.text('Course.number'))),
                get_label = lambda theCourse : f"{theCourse.number} - {theCourse.title}"
    )
    section =  StringField('Section', validators=[Length(min=1, max=5)])
    term = StringField('Term', validators=[Length(min=1, max=5), Regexp('^\d{4}[ABCDFS]$', message='Term should be a year followed by a term letter (Ex. 2024B).')])
    submit = SubmitField('Update')
