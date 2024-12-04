import os
import pytest
from app import create_app, db
from app.main.models import User, Student, Instructor, CourseSection, Course, Position
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
        courses = ['CS1001', 'CS2002', 'CS3003', 'CS4004']
        titles = ['Intro to CS', 'Data Structures', 'Algorithms', 'Software Engineering']
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
    db.session.add(student1)
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

def do_login(test_client, path , username, passwd):
    response = test_client.post(path,
                          data=dict(username= username, password=passwd, remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    #Students should update this assertion condition according to their own page content
    assert b"Welcome to CSAssist" in response.data

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
    do_login(test_client, path = '/user/login', username = 'test', passwd = '1234')

    do_logout(test_client, path = '/user/logout')

def test_create_coursection(test_client,init_database):
    do_login(test_client, path='/user/login', username='test', passwd='1234')

    response = test_client.get('/instructor/create_course')
    assert response.status_code == 200
    assert b"Create a course section" in response.data

    all_courses = db.session.scalars(sqla.select(Course)).all()
    print(all_courses)
    course = list( map(lambda t: t.id, all_courses[:1]))
    print(course)

    faculty = db.session.scalars(sqla.select(User).where(User.username == 'test')).first()

    response = test_client.post('/instructor/create_course',
                                data=dict(course_number=course, section='BL02', instructor_id=faculty.id,
                                          term='2024B'),
                                follow_redirects=True)


    assert response.status_code == 200
    #assert b"Welcome to CSAssist" in response.data
    course = db.session.scalars(sqla.select(CourseSection).where(CourseSection.course_number == 'CS1001').where(CourseSection.instructor_id == faculty.id)).first()
    print(course)
    assert course is not None
    assert b"The new course has successfully posted!" in response.data

    do_logout(test_client, path='/user/logout')

def test_create_position(test_client,init_database):
    do_login(test_client, path='/user/login', username='test', passwd='1234')
    # create course section
    response = test_client.post('/instructor/create_course',
                                data=dict(course_number='CS1001', section='BL02',
                                          term='2024B'),
                                follow_redirects=True)

    assert response.status_code == 200

    # create position
    db.session.add(CourseSection(course_number='CS1001', section='BL01', instructor_id=1, term='2024A'))
    db.session.commit()
    course = db.session.scalars(sqla.select(CourseSection).where(CourseSection.course_number == 'CS1001')).first()
    assert course is not None
    response = test_client.post('/instructor/'+str(course.id)+'/create_position',
                                data=dict(num_SAs=5, min_GPA=3.2,
                                          min_grade='B'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"The new position has been successfully added!" in response.data

    do_logout(test_client, path='/user/logout')


def test_apply_course(test_client, init_database):
    do_login(test_client, path='/user/login', username='gatorade', passwd='1234')

    db.session.add(CourseSection(course_number='CS1001', section='BL01', instructor_id=1, term='2024A'))
    db.session.add(Position(section_id=1, num_SAs=2))
    db.session.commit()
    position = db.session.scalars(sqla.select(Position).where(Position.section_id == 1)).first()
    assert position is not None

    response = test_client.get('/positions/'+str(position.id)+'/apply')
    assert response.status_code == 200
    assert b"Applying for position" in response.data

    response = test_client.post('/positions/'+str(position.id)+'/apply', 
                                data=dict(grade_aquired='A', term_taken='A23', 
                                          course_term='A24'),
                                follow_redirects=True)

    assert response.status_code == 200
    assert b"Welcome to CSAssist" in response.data

    do_logout(test_client, path='/user/logout')

def test_applications(test_client, init_database):
    do_login(test_client, path='/user/login', username='test', passwd='1234')

    db.session.add(CourseSection(course_number='CS1001', section='BL01', instructor_id=1, term='2024A'))
    db.session.add(Position(section_id=1, num_SAs=4, min_GPA=4.5, min_grade='A'))
    db.session.commit()
    pos = db.session.get(Position, 1)
    response = test_client.post('/applications/'+str(pos.id))
    assert response.status_code == 200

    data = eval(response.data)
    assert len(data) == 0


    do_logout(test_client, path='/user/logout')

