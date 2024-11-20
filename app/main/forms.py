from flask_wtf import FlaskForm
from app import db
import sqlalchemy as sqla
from wtforms import StringField, SubmitField, SelectField, TextAreaField, BooleanField, IntegerField, FloatField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import  ValidationError, DataRequired, Length
from app.main.models import Course, CourseSection
# from wtforms.widgets import ListWidget