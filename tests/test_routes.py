import os
import pytest
from app import create_app, db
from app.main.models import User, Student, Instructor
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


@pytest.fixture
def init_database():
    # Create the database and the database table
    db.create_all()
    #add a user
    user1 = new_user(uname='snow', uemail='snow@wpi.edu',passwd='1234', firstname='snow', lastname='snow', wpi_id='234234567', phone='8908907892')
    # Insert user data
    db.session.add(user1)
    # Commit the changes for the users
    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()

def test_instructor_register_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user/register' page is requested (GET)
    THEN check that the response is valid
    """
    # Create a test client using the Flask application configured for testing
    response = test_client.get('/instructor/register')
    assert response.status_code == 200
    assert b"Register" in response.data

def test_student_register_page(test_client):
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
    #assert b"Please log in to access this page." in response.data

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