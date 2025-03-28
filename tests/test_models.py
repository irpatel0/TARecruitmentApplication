import warnings
warnings.filterwarnings("ignore")

from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.main.models import User, Student, Instructor, Course, CourseSection, Position, Application, CourseTaken
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class TestModels(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='sam', email='sam@wpi.edu')
        u.set_password('sam123')
        self.assertFalse(u.get_password('123'))
        self.assertTrue(u.get_password('sam123'))

    def test_create_instructor(self):
        instructor = Instructor(username='tester',
                                firstname='testuser',
                                lastname='testuser',
                                wpi_id='456789012',
                                email='test@wpi.edu',
                                phone='9087096751')
        db.session.add(instructor)
        db.session.commit()
        self.assertEqual(instructor.user_type, 'Instructor')
        self.assertEqual(instructor.username, 'tester')
        self.assertEqual(instructor.email, 'test@wpi.edu')
        self.assertEqual(instructor.wpi_id, '456789012')
        self.assertEqual(instructor.phone, '9087096751')

    def test_create_student(self):
        student = Student(username='tester',
                                firstname='testuser',
                                lastname='testuser',
                                wpi_id='456789012',
                                email='test@wpi.edu',
                                phone='9087096751',
                                gpa=3.5,
                                graduation_date='2026'
                          )
        db.session.add(student)
        db.session.commit()
        self.assertEqual(student.user_type, 'Student')
        self.assertEqual(student.username, 'tester')
        self.assertEqual(student.email, 'test@wpi.edu')
        self.assertEqual(student.wpi_id, '456789012')
        self.assertEqual(student.phone, '9087096751')

    def test_create_course(self):
        course = Course(number='CS1010', title='Introduction to Programming')
        db.session.add(course)
        db.session.commit()
        self.assertEqual(course.number, 'CS1010')
        self.assertEqual(course.title, 'Introduction to Programming')

    def test_create_course_section(self):
        course = Course(number='CS1010', title='Introduction to Programming')
        db.session.add(course)
        db.session.commit()
        instructor = Instructor(username='professor', firstname='John', lastname='Doe', wpi_id='123456789', email='john.doe@wpi.edu', phone='1234567890')
        db.session.add(instructor)
        db.session.commit()
        course_section = CourseSection(course_number=course.number, section='A01', instructor_id=instructor.id, term='2023A')
        db.session.add(course_section)
        db.session.commit()
        self.assertEqual(course_section.course_number, course.number)
        self.assertEqual(course_section.section, 'A01')
        self.assertEqual(course_section.instructor_id, instructor.id)
        self.assertEqual(course_section.term, '2023A')

    def test_create_position(self):
        course = Course(number='CS1010', title='Introduction to Programming')
        db.session.add(course)
        db.session.commit()
        instructor = Instructor(username='professor', firstname='John', lastname='Doe', wpi_id='123456789', email='john.doe@wpi.edu', phone='1234567890')
        db.session.add(instructor)
        db.session.commit()
        course_section = CourseSection(course_number=course.id, section='A01', instructor_id=instructor.id, term='2023A')
        db.session.add(course_section)
        db.session.commit()
        position = Position(section_id=course_section.id, num_SAs=2, available=True, min_GPA=3.0, min_grade='B')
        db.session.add(position)
        db.session.commit()
        self.assertEqual(position.section_id, course_section.id)
        self.assertEqual(position.num_SAs, 2)
        self.assertTrue(position.available)
        self.assertEqual(position.min_GPA, 3.0)
        self.assertEqual(position.min_grade, 'B')

    def test_applications(self):
        # Create a student
        student = Student(username='student1', firstname='John', lastname='Doe', wpi_id='123456789', email='john.doe@example.com', phone='1234567890', graduation_date='2026')
        student.set_password('password')
        db.session.add(student)
        db.session.commit()

        # Create an instructor
        instructor = Instructor(username='instructor1', firstname='Jane', lastname='Smith', wpi_id='987654321', email='jane.smith@example.com', phone='0987654321')
        instructor.set_password('password')
        db.session.add(instructor)
        db.session.commit()

        # Create a course
        course = Course(number='CS101', title='Introduction to Computer Science')
        db.session.add(course)
        db.session.commit()

        # Create a course section
        course_section = CourseSection(course_number=course.id, section='A01', instructor_id=instructor.id, term='2023A')
        db.session.add(course_section)
        db.session.commit()

        # Create a position
        position = Position(section_id=course_section.id, num_SAs=2, available=True, min_GPA=3.0, min_grade='B')
        db.session.add(position)
        db.session.commit()

        # Create an application
        application = Application(grade_aquired='A', term_taken='2022A', status='Pending', position_id=position.id, student_id=student.id, applicant=student, applied_to=position)
        db.session.add(application)
        db.session.commit()

        position.applications.add(application)

        # Verify the application attributes
        self.assertEqual(student.applied_to(position.id), True)
        self.assertEqual(application.grade_aquired, 'A')
        self.assertEqual(application.term_taken, '2022A')
        self.assertEqual(application.status, 'Pending')
        self.assertEqual(application.applicant.id, student.id)
        self.assertEqual(application.applied_to.id, position.id)
        self.assertEqual(len(position.get_applications()), 1)
        self.assertEqual(position.get_applications()[0].student_id, application.student_id)
        self.assertEqual(position.get_applications()[0].position_id, application.position_id)
        self.assertEqual(application.get_only_student().id, student.id)
        self.assertEqual(application.get_only_student().username, student.username)

    def test_course_taken(self):

        #create course 
        course = Course(number='CS1010', title='Introduction to Programming')
        db.session.add(course)
        db.session.commit()

        #create student
        student = Student(username='student1', firstname='John', lastname='Doe', wpi_id='123456789', email='john.doe@example.com', phone='1234567890', graduation_date='2026')
        student.set_password('password')
        db.session.add(student)
        db.session.commit()

        #create a course taken by a student
        course_taken = CourseTaken(student_id=student.id, course_id=course.id, grade='A')
        db.session.add(course_taken)
        db.session.commit()

        self.assertEqual(course_taken.course_id, course.id)
        self.assertEqual(course_taken.student_id, student.id)
        self.assertEqual(course_taken.grade, 'A')


    def test_past_enrollments(self):
        student = Student(username='student1', firstname='John', lastname='Doe', wpi_id='123456789', email='john.doe@example.com', phone='1234567890', graduation_date='2026')
        student.set_password('password')
        db.session.add(student)
        db.session.commit()

        course = Course(number='CS1010', title='Introduction to Programming')
        db.session.add(course)
        db.session.commit()

        student.taught.add(course)
        db.session.commit()

        course_taken = CourseTaken(student_id=student.id, course_id=course.id, grade='A')
        db.session.add(course_taken)
        db.session.commit()

        student.courses_taken.add(course_taken)

        self.assertEqual(len(student.get_taught()), 1)
        self.assertEqual(student.get_taught()[0].number, 'CS1010')
        self.assertEqual(student.get_taught()[0].title, 'Introduction to Programming')
        self.assertEqual(len(student.get_taken()), 1)
        self.assertEqual(student.get_taken()[0].course_id, course.id)


    def test_get_assigned_students(self):
                # Create a student
        student = Student(username='student1', firstname='John', lastname='Doe', wpi_id='123456789', email='john.doe@example.com', phone='1234567890', graduation_date='2026')
        student.set_password('password')
        db.session.add(student)
        db.session.commit()

        # Create an instructor
        instructor = Instructor(username='instructor1', firstname='Jane', lastname='Smith', wpi_id='987654321', email='jane.smith@example.com', phone='0987654321')
        instructor.set_password('password')
        db.session.add(instructor)
        db.session.commit()

        # Create a course
        course = Course(number='CS101', title='Introduction to Computer Science')
        db.session.add(course)
        db.session.commit()

        # Create a course section
        course_section = CourseSection(course_number=course.id, section='A01', instructor_id=instructor.id, term='2023A')
        db.session.add(course_section)
        db.session.commit()

        course_section.assigned_students.add(student)
        
        self.assertEqual(len(course_section.get_assignedStudents()), 1)
        self.assertEqual(course_section.get_assignedStudents()[0].username, 'student1')
        self.assertEqual(course_section.get_assignedStudents()[0].email, 'john.doe@example.com')

    def test_recommendation_score(self):
        # Create a student
        student = Student(username='student1', firstname='John', lastname='Doe', wpi_id='123456789', email='john.doe@example.com', phone='1234567890', graduation_date='2026')
        student.set_password('password')
        db.session.add(student)
        db.session.commit()

        # Create an instructor
        instructor = Instructor(username='instructor1', firstname='Jane', lastname='Smith', wpi_id='987654321', email='jane.smith@example.com', phone='0987654321')
        instructor.set_password('password')
        db.session.add(instructor)
        db.session.commit()

        # Create a course
        course = Course(number='CS101', title='Introduction to Computer Science')
        db.session.add(course)
        db.session.commit()

        # Create a course section
        course_section = CourseSection(course_number=course.number, section='A01', instructor_id=instructor.id, term='2023A')
        db.session.add(course_section)
        db.session.commit()

        # Create a position
        position = Position(section_id=course_section.id, num_SAs=2, available=True, min_GPA=3.0, min_grade='B')
        db.session.add(position)
        db.session.commit()

        # test if recommendation score is zero when student has not taken the course
        self.assertEqual(position.recommendation_score(student), 0)

        #Add course taken by student
        course_taken = CourseTaken(student_id=student.id, course_id=course.id, grade='A')
        db.session.add(course_taken)
        db.session.commit()

        # test if recommendation score when student has taken the course and scored A, but has not taught it or meet gpa
        self.assertEqual(position.recommendation_score(student), 6)
        #test is recomendation score when student has taken and taught class but does not meet gpa
        student.taught.add(course)
        db.session.commit()
        self.assertEqual(position.recommendation_score(student), 9)
        #test if recommendation score when student has taken and taught class and meets gpa
        student.gpa = 3.5
        db.session.commit()
        self.assertEqual(position.recommendation_score(student), 11)


#python -m unittest -v tests//test_models.py
#pytest -v tests//test_routes.py