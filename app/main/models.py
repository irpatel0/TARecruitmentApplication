from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo
from flask_login import UserMixin
from app import login
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import ARRAY


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

assignedTerms = db.Table(
    'assignedTerms',
    db.metadata,
    sqla.Column('student_id', sqla.Integer, sqla.ForeignKey('student.id'), primary_key=True),
    sqla.Column('coursesection_id', sqla.Integer, sqla.ForeignKey('coursesection.id'), primary_key=True)
)

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
    #MAKE a an Attribute called --> assigned_terms : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(5)) --> used for referencing terms
    #assigned_terms : sqlo.Mapped[list[str]] = sqlo.mapped_column(ARRAY(str), default=list)
    __mapper_args__ = {'polymorphic_identity': 'Student'}

    #relationships
    taught : sqlo.WriteOnlyMapped['Course'] = sqlo.relationship(
            secondary=pastEnrollments, 
            primaryjoin=(pastEnrollments.c.student_id == id),
            back_populates='taught_by',
        )
    student_applications : sqlo.WriteOnlyMapped['Application'] = sqlo.relationship(back_populates='applicant')
    courses_taken : sqlo.WriteOnlyMapped['CourseTaken'] = sqlo.relationship(back_populates='student')

    
    assigned_terms : sqlo.WriteOnlyMapped['CourseSection'] = sqlo.relationship(
        secondary = assignedTerms,
        primaryjoin=(assignedTerms.c.student_id == id),
        back_populates='assigned_students' ) 
    


    def applied_to(self, position_id):
        return db.session.scalars(sqla.select(Application).where(Application.student_id == self.id).where(Application.position_id == position_id)).first() is not None

    def get_taught(self):
        return db.session.scalars(self.taught.select()).all()
    
    def get_taken(self):
        return db.session.scalars(self.courses_taken.select()).all()
    
    def get_assigned(self):
        return db.session.scalars(self.assigned_terms.select()).all()


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
    sections : sqlo.WriteOnlyMapped['CourseSection'] = sqlo.relationship(back_populates='course')
    students_taken : sqlo.WriteOnlyMapped['CourseTaken'] = sqlo.relationship(back_populates='course')


class CourseSection(db.Model):
    __tablename__ = 'coursesection'
    id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, primary_key=True)
    course_number : sqlo.Mapped[str] = sqlo.mapped_column(sqla.ForeignKey(Course.number))
    section : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(5))
    instructor_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Instructor.id))
    term : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(5))
    #relations
    position : sqlo.Mapped['Position'] = sqlo.relationship(back_populates='course_section', passive_deletes=True)
    professor : sqlo.Mapped['Instructor'] = sqlo.relationship(back_populates='course_sections')
    course : sqlo.Mapped['Course'] = sqlo.relationship(back_populates='sections')

    assigned_students : sqlo.WriteOnlyMapped['Student'] = sqlo.relationship(
        secondary = assignedTerms,
        primaryjoin=(assignedTerms.c.coursesection_id == id),
        back_populates='assigned_terms',
        passive_deletes=True ) 

    def get_assignedStudents(self):
        assigned_students = db.session.scalars(self.assigned_students.select()).all()
        if assigned_students is None: 
            return "This course section has no assigned Student Assistants"
        else:
            return assigned_students


    def hasPosition(self):
        return self.position is not None
    
    def __repr__(self):
        return f'{self.course_number} - {self.section} - {self.term}'

class Position(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, primary_key=True)
    section_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(CourseSection.id))
    num_SAs : sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, default=0)
    num_Assigned : sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, default=0) #sqlo.mapped_collection(sqla.Integer) --> WAS PREVIOUSLY THIS
    available : sqlo.Mapped[bool] = sqlo.mapped_column(sqla.Boolean, default=True)
    min_GPA : sqlo.Mapped[float] = sqlo.mapped_column(sqla.Float, default=0)
    min_grade : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(2), default='A')
    timestamp : sqlo.Mapped[datetime] = sqlo.mapped_column(default = lambda : datetime.now(timezone.utc))
    # relationships
    course_section : sqlo.Mapped['CourseSection'] = sqlo.relationship(back_populates='position')
    applications : sqlo.WriteOnlyMapped['Application'] = sqlo.relationship(back_populates='applied_to', passive_deletes=True)


    def get_applications(self):
        return db.session.scalars(self.applications.select()).all()
    
    def recommendation_score(self, student):
        course_section = db.session.get(CourseSection, self.section_id)
        course = db.session.scalars(sqla.select(Course).where(Course.number == course_section.course_number)).first()
        enrollment = db.session.scalars(sqla.select(CourseTaken).where(CourseTaken.student_id == student.id)
                                                                .where(CourseTaken.course_id == course.id)).first()
        
        score = 0
        grade_map = {'A': 5, 'B': 4, 'C': 3, 'D': 2, 'F': 1, 'NR': 0}

        if student.gpa >= self.min_GPA:
            score += 2
        if course in student.get_taught():
            score += 3

        print(student.get_taken())
        for course_taken in student.get_taken():
            print(course_taken)
            enrolled_course = db.session.scalars(sqla.select(Course).where(Course.id == course_taken.course_id)).first()
            if (enrolled_course == course):
                score += 2

                if grade_map.get(enrollment.grade, 0) >= grade_map.get(self.min_grade, 0):
                    score += 2

                if grade_map.get(enrollment.grade, 0) == 5:
                    score += 2

        return float(score)


    def __repr__(self):
        course_number = self.course_section.course_number
        course_term = self.course_section.term
        return f'{course_number} - {self.course_section.section} - {course_term}'
    

class Application(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, primary_key=True)
    student_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Student.id))
    position_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Position.id))
    grade_aquired : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(2), default='A')
    term_taken : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(5))
    # course_term : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(5))
    status : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(20), default='Pending')

    #relations
    applicant : sqlo.Mapped[Student] = sqlo.relationship(back_populates='student_applications')
    applied_to : sqlo.Mapped[Position] = sqlo.relationship(back_populates='applications')

    def get_student(self):
        return db.session.scalars(sqla.select(User).where(User.id == self.student_id)).first()

    def get_only_student(self):
        return db.session.scalars(sqla.select(Student).where(Student.id == self.student_id)).first()
    

class CourseTaken(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, primary_key=True)
    student_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Student.id))
    course_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Course.id))
    grade : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(2))

    #relations
    student : sqlo.Mapped[Student] = sqlo.relationship(back_populates='courses_taken')
    course : sqlo.Mapped[Course] = sqlo.relationship(back_populates='students_taken')