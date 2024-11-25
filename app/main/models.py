from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo
from flask_login import UserMixin
from app import login
from datetime import datetime, timezone


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

pastEnrollments = db.Table(
    'pastEnrollments',
    db.metadata,
    sqla.Column('student_id', sqla.Integer, sqla.ForeignKey('student.id'), primary_key=True),
    sqla.Column('course_id', sqla.Integer, sqla.ForeignKey('course.id'), primary_key=True)
)

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
    graduation_date : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(4))
    assigned : sqlo.Mapped[bool] = sqlo.mapped_column(sqla.Boolean, default=False)

    __mapper_args__ = {'polymorphic_identity': 'Student'}

    #relationships
    taught : sqlo.WriteOnlyMapped['Course'] = sqlo.relationship(
            secondary=pastEnrollments, 
            primaryjoin=(pastEnrollments.c.student_id == id),
            back_populates='taught_by',
        )
    student_applications : sqlo.WriteOnlyMapped['Application'] = sqlo.relationship(back_populates='applicant')

class Instructor(User):
    __tablename__ = 'instructor'
    id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(User.id), primary_key=True)
    course_sections : sqlo.Mapped['CourseSection'] = sqlo.relationship(back_populates='professor')

    __mapper_args__ = {'polymorphic_identity': 'Instructor'}

class Course(db.Model):
    __tablename__ = 'course'
    id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, primary_key=True)
    number: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(7), unique=True)
    title : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(120))

    #relationships
    taught_by : sqlo.WriteOnlyMapped['Student'] = sqlo.relationship(
            secondary=pastEnrollments, 
            primaryjoin=(pastEnrollments.c.course_id == id),
            back_populates='taught',
    )


class CourseSection(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, primary_key=True)
    course_number : sqlo.Mapped[str] = sqlo.mapped_column(sqla.ForeignKey(Course.id))
    section : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(5))
    instructor_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Instructor.id))
    term : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(5))
    #relations
    position : sqlo.Mapped['Position'] = sqlo.relationship(back_populates='course_section')
    professor : sqlo.Mapped['Instructor'] = sqlo.relationship(back_populates='course_sections')
    course = db.relationship('Course', backref='course_sections')

    def hasPosition(self):
        return self.position is not None
    
    def __repr__(self):
        return f'{self.course_number} - {self.section} - {self.term}'

class Position(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, primary_key=True)
    section_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(CourseSection.id))
    num_SAs : sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer)
    available : sqlo.Mapped[bool] = sqlo.mapped_column(sqla.Boolean, default=True)
    min_GPA : sqlo.Mapped[float] = sqlo.mapped_column(sqla.Float, default=0)
    min_grade : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(2), default='A')
    timestamp : sqlo.Mapped[datetime] = sqlo.mapped_column(default = lambda : datetime.now(timezone.utc))
    # relationships
    course_section = db.relationship('CourseSection', backref='positions')
    applications : sqlo.WriteOnlyMapped['Application'] = sqlo.relationship(back_populates='applied_to')

    def get_applications(self):
        return db.session.scalars(self.applications.select()).all()

    def __repr__(self):
        course_number = self.course_section.course_number
        course_term = self.course_section.term
        return f'{course_number} - {self.course_section.section} - {course_term}'
    

class Application(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, primary_key=True)
    student_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey('student.id'))
    position_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey('position.id'))
    grade_aquired : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(2), default='A')
    term_taken : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(5))
    course_term : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(5))
    status : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(20), default='Pending')

    #relations
    applicant : sqlo.Mapped[Student] = sqlo.relationship(back_populates='student_applications')
    applied_to : sqlo.Mapped[Position] = sqlo.relationship(back_populates='applications')

