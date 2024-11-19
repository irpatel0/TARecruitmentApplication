from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo
from flask_login import UserMixin
from app import login

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    username : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(64), index=True, unique=True)
    firstname : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(120))
    lastname : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(120))
    wpi_id : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(9), default=0, unique=True)
    email : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(120), unique=True)
    phone : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(10), unique=True)
    password_hash: sqlo.Mapped[Optional[str]] = sqlo.mapped_column(sqla.String(256))
    user_type : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(50))

    __mapper_args__ = {'polymorphic_identity': 'User',
                       'polymorphic_on': user_type}

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password_hash, password)

class Student(User):
    __tablename__ = 'student'
    id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(User.id), primary_key=True)
    gpa : sqlo.Mapped[float] = sqlo.mapped_column(sqla.Float, default=0)
    # TODO: courses taught
    graduation_date : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(4))

    __mapper_args__ = {'polymorphic_identity': 'Student'}

class Instructor(User):
    __tablename__ = 'instructor'
    id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(User.id), primary_key=True)
    course_sections : sqlo.Mapped['CourseSection'] = sqlo.relationship(back_populates='professor')

    __mapper_args__ = {'polymorphic_identity': 'Instructor'}

class Course(db.Model):
    number: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(7), primary_key=True)
    title : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(120))


class CourseSection(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, primary_key=True)
    course_number : sqlo.Mapped[str] = sqlo.mapped_column(sqla.ForeignKey(Course.number))
    section : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(5))
    instructor_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Instructor.id))
    term : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(5))

    #relations
    professor : sqlo.Mapped['Instructor'] = sqlo.relationship(back_populates='course_sections')
    course = db.relationship('Course', backref='course_sections')

class Position(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, primary_key=True)
    section_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(CourseSection.id))
    num_SAs : sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer)
    available : sqlo.Mapped[bool] = sqlo.mapped_column(sqla.Boolean, default=True)
    min_GPA : sqlo.Mapped[float] = sqlo.mapped_column(sqla.Float, default=0)
    min_grade : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(2), default='A')
    course_section = db.relationship('CourseSection', backref='positions')
    def __repr__(self):
        course_number = self.course_section.course.number
        return f'Position for {course_number}'
