import os
import pytest
from app import create_app, db
from app.main.models import User, Student, Instructor, CourseSection, Course, Position, CourseTaken
from config import Config
import sqlalchemy as sqla


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = 'bad-bad-key'
    WTF_CSRF_ENABLED = False
    DEBUG = True
    TESTING = True


@pytest.fixture(scope='module')
def test_client():
    # create the flask application ; configure the app for tests
    flask_app = create_app(config_class=TestConfig)

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client
    # this is where the testing happens!

    ctx.pop()


def new_user(uname, uemail, passwd, firstname, lastname, wpi_id, phone):
    user = User(username=uname, email=uemail, firstname=firstname, lastname=lastname, wpi_id=wpi_id, phone=phone)
    user.set_password(passwd)
    return user

def new_student(uname, uemail, passwd, firstname, lastname, wpi_id, phone, gpa, graduation_date):
    student = Student(username=uname, email=uemail, firstname=firstname, lastname=lastname, wpi_id=wpi_id, phone=phone, gpa=gpa, graduation_date=graduation_date)
    student.set_password(passwd)
    return student

def new_instructor(uname, uemail, passwd, firstname, lastname, wpi_id, phone):
    instructor = Instructor(username=uname, email=uemail, firstname=firstname, lastname=lastname, wpi_id=wpi_id, phone=phone)
    instructor.set_password(passwd)
    return instructor

def init_courses():
    count = db.session.scalar(db.select(db.func.count(Course.id)))
    if count == 0:
        courses = ['CS1101', 'CS2102', 'CS2223', 'CS2303', 'CS3013', 'CS 3133', 'CS3431', 'CS3733', 'CS4341', 'CS4241',
                   'CS4342', 'CS4433']
        titles = ['Introduction To Program Design', 'Object-Oriented Design Concepts', 'Algorithms',
                  'Systems Programming Concepts', 'Operating Systems', 'Foundations Of Computer Science',
                  'Database Systems I', 'Software Engineering', 'Introduction To Artificial Intelligence',
                  'Webware: Computational Technology For Network Information Systems', 'Machine Learning',
                  'Big Data Management and Analytics']
        for i in range(len(courses)):
            db.session.add(Course(number=courses[i], title=titles[i]))
        db.session.commit()
    return None

@pytest.fixture
def init_database():
    # Create the database and the database table
    db.create_all()
    init_courses()

    #add a user
    user1 = new_user(uname='snow', uemail='snow@wpi.edu',passwd='1234', firstname='snow', lastname='snow', wpi_id='234234567', phone='8908907892')
    student1 = new_student(uname='gatorade', uemail='gatorade@wpi.edu', passwd='1234', firstname='gatorade', lastname='gatorade', wpi_id='123456789', phone='1234567890', gpa='2.0', graduation_date='2025')
    instructor1 = new_instructor(uname='test', uemail='test@wpi.edu',passwd='1234', firstname='test', lastname='test', wpi_id='234234568', phone='8908907893')
    # Insert user data
    db.session.add(user1)
    db.session.commit()
    db.session.add(student1)
    db.session.commit()
    db.session.add(instructor1)
    # Commit the changes for the users
    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()

def test_instructor_register_page(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user/register' page is requested (GET)
    THEN check that the response is valid
    """
    # Create a test client using the Flask application configured for testing
    response = test_client.get('/instructor/register')
    assert response.status_code == 200
    assert b"Register" in response.data

def test_student_register_page(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user/register' page is requested (GET)
    THEN check that the response is valid
    """
    # Create a test client using the Flask application configured for testing
    response = test_client.get('/student/studentregister')
    assert response.status_code == 200
    assert b"Register" in response.data


def test_register(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user/register' form is submitted (POST)
    THEN check that the response is valid and the database is updated correctly
    """
    # Create a test client using the Flask application configured for testing
    response = test_client.post('/instructor/register',
                                data=dict(username='john', email='john@wpi.edu', password="bad",
                                          password2="bad", first_name='john', last_name='john', wpi_id='123908765', phone='3407809016'),
                                follow_redirects=True)
    assert response.status_code == 200

    s = db.session.scalars(sqla.select(User).where(User.username == 'john')).first()
    s_count = db.session.scalar(sqla.select(db.func.count()).where(User.username == 'john'))

    assert s.email == 'john@wpi.edu'
    assert s_count == 1
    assert s.user_type == 'Instructor'
    assert s.wpi_id == '123908765'
    assert b"Welcome to CSAssist" in response.data
    assert b"Please log in to access this page." in response.data

def test_invalidlogin(test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user/login' form is submitted (POST) with wrong credentials
    THEN check that the response is valid and login is refused
    """
    response = test_client.post('/user/login',
                          data=dict(username='snow', password='12345',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Invalid username or password!" in response.data

def instructor_do_login(test_client, path , username, passwd):
    response = test_client.post(path,
                          data=dict(username= username, password=passwd, remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Welcome Instructor -" in response.data

def student_do_login(test_client, path , username, passwd):
    response = test_client.post(path,
                          data=dict(username= username, password=passwd, remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Welcome Student -" in response.data

def do_logout(test_client, path):
    response = test_client.get(path,
                          follow_redirects = True)
    assert response.status_code == 200
    # Assuming the application re-directs to login page after logout.
    #Students should update this assertion condition according to their own page content
    assert b"Sign In" in response.data
    assert b"Welcome to CSAssist" in response.data
# ------------------------------------

def test_login_logout(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user/login' form is submitted (POST) with correct credentials
    THEN check that the response is valid and login is succesfull
    """
    assert test_client is not None
    # assert init_database is not None
    instructor_do_login(test_client, path = '/user/login', username = 'test', passwd = '1234')

    do_logout(test_client, path = '/user/logout')

def test_create_coursection(test_client,init_database):
    instructor_do_login(test_client, path='/user/login', username='test', passwd='1234')

    response = test_client.get('/instructor/create_course')
    assert response.status_code == 200
    assert b"Create a course section" in response.data

    all_courses = db.session.scalars(sqla.select(Course)).all()
    course = list( map(lambda t: t.id, all_courses[:1]))
    faculty = db.session.scalars(sqla.select(User).where(User.username == 'test')).first()

    response = test_client.post('/instructor/create_course',
                                data=dict(course_number=course, section='BL02', instructor_id=faculty.id,
                                          year='2024', term='B'),
                                follow_redirects=True)


    assert response.status_code == 200

    course = db.session.scalars(sqla.select(CourseSection).where(CourseSection.course_number == 'CS1101').where(CourseSection.instructor_id == faculty.id)).all()
    assert len(course) == 1
    assert course is not None
    assert course[0].course_number == 'CS1101'
    assert course[0].section == 'BL02'
    assert course[0].term == '2024B'
    assert b"The new course has successfully posted!" in response.data

    do_logout(test_client, path='/user/logout')

def test_create_position(test_client,init_database):
    instructor_do_login(test_client, path='/user/login', username='test', passwd='1234')
    # create course section
    all_courses = db.session.scalars(sqla.select(Course)).all()
    course = list(map(lambda t: t.id, all_courses[:1]))
    faculty = db.session.scalars(sqla.select(User).where(User.username == 'test')).first()

    response = test_client.post('/instructor/create_course',
                                data=dict(course_number=course, section='BL02', instructor_id=faculty.id,
                                          year='2024', term='B'),
                                follow_redirects=True)

    assert response.status_code == 200

    # create position
    course = db.session.scalars(sqla.select(CourseSection).where(CourseSection.course_number == 'CS1101')).first()
    assert course is not None
    response = test_client.post('/instructor/'+str(course.id)+'/create_position',
                                data=dict(num_SAs=5, min_GPA=3.2,
                                          min_grade='B'),
                                follow_redirects=True)

    assert response.status_code == 200
    pos = course.position
    assert pos.num_SAs == 5
    assert pos.min_GPA == 3.2
    assert pos.min_grade == 'B'
    assert b"The new position has been successfully added!" in response.data

    do_logout(test_client, path='/user/logout')


def test_apply_course(test_client, init_database):
    instructor_do_login(test_client, path='/user/login', username='test', passwd='1234')
    # create course section
    all_courses = db.session.scalars(sqla.select(Course)).all()
    course = list(map(lambda t: t.id, all_courses[:1]))
    faculty = db.session.scalars(sqla.select(User).where(User.username == 'test')).first()

    response = test_client.post('/instructor/create_course',
                                data=dict(course_number=course, section='BL02', instructor_id=faculty.id,
                                          year='2024', term='B'),
                                follow_redirects=True)

    assert response.status_code == 200

    # create position
    course = db.session.scalars(sqla.select(CourseSection).where(CourseSection.course_number == 'CS1101')).first()
    assert course is not None
    response = test_client.post('/instructor/' + str(course.id) + '/create_position',
                                data=dict(num_SAs=5, min_GPA=3.2,
                                          min_grade='B'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"The new position has been successfully added!" in response.data

    do_logout(test_client, path='/user/logout')

    student_do_login(test_client, path='/user/login', username='gatorade', passwd='1234')

    course = db.session.scalars(sqla.select(CourseSection).where(CourseSection.course_number == 'CS1101')).first()
    position = course.position
    assert position is not None

    response = test_client.get('/positions/'+str(position.id)+'/apply')
    assert response.status_code == 200
    assert b"Applying for position" in response.data

    response = test_client.post('/positions/'+str(position.id)+'/apply',
                                data=dict(grade='A', year_taken = '2023', term_taken='A'),
                                follow_redirects=True)

    apps = position.get_applications()
    assert response.status_code == 200
    assert len(apps) == 1
    assert apps[0].grade_aquired == 'A'
    assert apps[0].term_taken == '2023A'
    assert b"Welcome Student -" in response.data
    assert b"You have successfully applied for the course!" in response.data

    do_logout(test_client, path='/user/logout')

def test_applications(test_client, init_database):
    instructor_do_login(test_client, path='/user/login', username='test', passwd='1234')
    # create course section
    all_courses = db.session.scalars(sqla.select(Course)).all()
    course = list(map(lambda t: t.id, all_courses[:1]))
    faculty = db.session.scalars(sqla.select(User).where(User.username == 'test')).first()

    response = test_client.post('/instructor/create_course',
                                data=dict(course_number=course, section='BL02', instructor_id=faculty.id,
                                          year='2024', term='B'),
                                follow_redirects=True)

    assert response.status_code == 200

    # create position
    course = db.session.scalars(sqla.select(CourseSection).where(CourseSection.course_number == 'CS1101')).first()
    assert course is not None
    response = test_client.post('/instructor/' + str(course.id) + '/create_position',
                                data=dict(num_SAs=5, min_GPA=3.2,
                                          min_grade='B'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"The new position has been successfully added!" in response.data

    do_logout(test_client, path='/user/logout')

    student_do_login(test_client, path='/user/login', username='gatorade', passwd='1234')

    course = db.session.scalars(sqla.select(CourseSection).where(CourseSection.course_number == 'CS1101')).first()
    position = course.position
    assert position is not None

    response = test_client.post('/positions/' + str(position.id) + '/apply',
                                data=dict(grade='A', year_taken='2023', term_taken='A'),
                                follow_redirects=True)

    assert response.status_code == 200
    assert b"Welcome Student -" in response.data

    do_logout(test_client, path='/user/logout')

    instructor_do_login(test_client, path='/user/login', username='test', passwd='1234')

    course = db.session.scalars(sqla.select(CourseSection).where(CourseSection.course_number == 'CS1101')).first()
    position = course.position
    response = test_client.post('/applications/'+str(position.id))
    assert response.status_code == 200

    data = eval(response.data)
    assert len(data) != 0
    assert data[0]['term_taken'] == '2023A'
    assert data[0]['grade_acquired'] == 'A'
    assert data[0]['status'] == 'Pending'
    assert data[0]['availability'] == 'Unassigned'


    do_logout(test_client, path='/user/logout')


def test_accept_student(test_client, init_database):
    instructor_do_login(test_client, path='/user/login', username='test', passwd='1234')
    # create course section
    all_courses = db.session.scalars(sqla.select(Course)).all()
    course = list(map(lambda t: t.id, all_courses[:1]))
    faculty = db.session.scalars(sqla.select(User).where(User.username == 'test')).first()

    response = test_client.post('/instructor/create_course',
                                data=dict(course_number=course, section='BL02', instructor_id=faculty.id,
                                          year='2024', term='B'),
                                follow_redirects=True)

    assert response.status_code == 200

    # create position
    course = db.session.scalars(sqla.select(CourseSection).where(CourseSection.course_number == 'CS1101')).first()
    assert course is not None
    response = test_client.post('/instructor/' + str(course.id) + '/create_position',
                                data=dict(num_SAs=5, min_GPA=3.2,
                                          min_grade='B'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"The new position has been successfully added!" in response.data

    do_logout(test_client, path='/user/logout')

    student_do_login(test_client, path='/user/login', username='gatorade', passwd='1234')

    course = db.session.scalars(sqla.select(CourseSection).where(CourseSection.course_number == 'CS1101')).first()
    position = course.position
    assert position is not None

    response = test_client.post('/positions/' + str(position.id) + '/apply',
                                data=dict(grade='A', year_taken='2023', term_taken='A'),
                                follow_redirects=True)

    assert response.status_code == 200
    assert b"Welcome Student -" in response.data

    do_logout(test_client, path='/user/logout')

    instructor_do_login(test_client, path = '/user/login', username = 'test', passwd = '1234')

    student = db.session.scalars(sqla.select(Student).where(Student.username == 'gatorade')).first()

    response = test_client.post('/position/'+str(position.id)+'/student/'+str(student.id)+'/accept',data={},
                          follow_redirects = True)

    assert response.status_code == 200
    assert b"Student successfully assigned to SA position" in response.data
    assert position.num_Assigned != 0

    student_assignedTerms = db.session.scalars(student.assigned_terms.select()).all()
    student_assignedTerm = 0
    for assignedTerm in student_assignedTerms:
        if assignedTerm.term == '2024B':
            student_assignedTerm = assignedTerm.term

    assert student_assignedTerm == '2024B'

    student_applications = db.session.scalars(student.student_applications.select()).all()
    student_application = 0
    for application in student_applications:
        if application.position_id == position.id:
            student_application = application

    assert student_application.status == 'Approved'

    student_enrollments = db.session.scalars(student.taught.select()).all()
    section_studentenrollments = db.session.scalars(student_enrollments[0].sections.select()).all()
    assert course.course_number == section_studentenrollments[0].course_number
    assert course.section == section_studentenrollments[0].section
    assert course.term == section_studentenrollments[0].term


def test_reject_student(test_client, init_database):
    instructor_do_login(test_client, path='/user/login', username='test', passwd='1234')
    # create course section
    all_courses = db.session.scalars(sqla.select(Course)).all()
    course = list(map(lambda t: t.id, all_courses[:1]))
    faculty = db.session.scalars(sqla.select(User).where(User.username == 'test')).first()

    response = test_client.post('/instructor/create_course',
                                data=dict(course_number=course, section='BL02', instructor_id=faculty.id,
                                          year='2024', term='B'),
                                follow_redirects=True)

    assert response.status_code == 200

    # create position
    course = db.session.scalars(sqla.select(CourseSection).where(CourseSection.course_number == 'CS1101')).first()
    assert course is not None
    response = test_client.post('/instructor/' + str(course.id) + '/create_position',
                                data=dict(num_SAs=5, min_GPA=3.2,
                                          min_grade='B'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"The new position has been successfully added!" in response.data

    do_logout(test_client, path='/user/logout')

    student_do_login(test_client, path='/user/login', username='gatorade', passwd='1234')

    course = db.session.scalars(sqla.select(CourseSection).where(CourseSection.course_number == 'CS1101')).first()
    position = course.position
    assert position is not None

    response = test_client.post('/positions/' + str(position.id) + '/apply',
                                data=dict(grade='A', year_taken='2023', term_taken='A'),
                                follow_redirects=True)

    assert response.status_code == 200
    assert b"Welcome Student -" in response.data

    do_logout(test_client, path='/user/logout')

    instructor_do_login(test_client, path='/user/login', username='test', passwd='1234')

    student = db.session.scalars(sqla.select(Student).where(Student.username == 'gatorade')).first()

    response = test_client.post('/position/'+str(position.id)+'/student/'+str(student.id)+'/reject',data={},
                          follow_redirects = True)

    assert response.status_code == 200

    student_applications = db.session.scalars(student.student_applications.select()).all()
    student_application = 0
    for application in student_applications:
        if application.position_id == position.id:
            student_application = application

    assert student_application.status == 'Rejected'
    assert b"Student application status updated to rejected" in response.data





def test_view_closedpositions(test_client, init_database):
    instructor_do_login(test_client, path='/user/login', username='test', passwd='1234')
    # create course section
    all_courses = db.session.scalars(sqla.select(Course)).all()
    course = list(map(lambda t: t.id, all_courses[:1]))
    faculty = db.session.scalars(sqla.select(User).where(User.username == 'test')).first()

    response = test_client.post('/instructor/create_course',
                                data=dict(course_number=course, section='BL02', instructor_id=faculty.id,
                                          year='2024', term='B'),
                                follow_redirects=True)

    assert response.status_code == 200

    # create position
    course = db.session.scalars(sqla.select(CourseSection).where(CourseSection.course_number == 'CS1101')).first()
    assert course is not None
    response = test_client.post('/instructor/' + str(course.id) + '/create_position',
                                data=dict(num_SAs=1, min_GPA=3.2,
                                          min_grade='B'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"The new position has been successfully added!" in response.data

    do_logout(test_client, path='/user/logout')

    student_do_login(test_client, path='/user/login', username='gatorade', passwd='1234')

    course = db.session.scalars(sqla.select(CourseSection).where(CourseSection.course_number == 'CS1101')).first()
    position = course.position
    assert position is not None

    response = test_client.post('/positions/' + str(position.id) + '/apply',
                                data=dict(grade='A', year_taken='2023', term_taken='A'),
                                follow_redirects=True)

    assert response.status_code == 200
    assert b"Welcome Student -" in response.data

    do_logout(test_client, path='/user/logout')

    instructor_do_login(test_client, path='/user/login', username='test', passwd='1234')

    student = db.session.scalars(sqla.select(Student).where(Student.username == 'gatorade')).first()

    response = test_client.post('/position/' + str(position.id) + '/student/' + str(student.id) + '/accept', data={},
                                follow_redirects=True)

    response = test_client.get('/instructor/closedpositions')
    assert response.status_code == 200
    assert b"Closed Course Sections" in response.data
    assert b"CS1101 - BL02 - 2024B" in response.data
    assert b"gatorade gatorade" in response.data


