import warnings
warnings.filterwarnings("ignore")

from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.main.models import User, Student, Instructor
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
