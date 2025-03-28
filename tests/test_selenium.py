import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from time import sleep

from app import create_app, db
from app.main.models import User, Student, Instructor, CourseSection, Course, Position
from config import Config
import sqlalchemy as sqla


@pytest.fixture
def instructor1():
    return {'username': 'john', 'email': 'john@wpi.edu', 'firstname': 'john', 'lastname': 'john', 'wpi_id': '345345345', 'phone': '1231231231', 'password':'strongpassword'}

@pytest.fixture
def student1():
    return {'username': 'sam', 'email': 'sam@wpi.edu', 'firstname': 'sam', 'lastname': 'sam', 'wpi_id': '345345678',
            'phone': '1231231890', 'password': 'alsostrongpassword', 'gpa': 4.0, 'graduation_date': '2026', 'course': 'CS 3733 - Software Engineering', 'grade': 'A'}

@pytest.fixture
def coursection():
    return {'course_number': 'CS3733', 'section': 'BL01', 'year': '2025', 'term': 'C-Term'}

@pytest.fixture
def position():
    return {'num_SAs': 3, 'min_GPA': 3.5, 'min_grade': 'B' }

@pytest.fixture
def apply():
    return {'grade': 'B', 'year_taken': '2024', 'term_taken': 'B'}

@pytest.fixture
def browser():
    CHROME_PATH = "C:\\Webdriver\\chromedriver-win64"
    print(CHROME_PATH)

    service = Service(executable_path=CHROME_PATH + '\\chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(8)

    yield driver

    # For cleanup, quit the driver
    driver.quit()


def test_register_instructor(browser,instructor1):

    browser.get('http://localhost:5000/instructor/register')
    # Enable this to maximize the window
    browser.maximize_window()
    browser.find_element(By.NAME, "first_name").send_keys(instructor1['firstname'])
    sleep(2)
    browser.find_element(By.NAME, "last_name").send_keys(instructor1['lastname'])
    sleep(2)
    browser.find_element(By.NAME, "wpi_id").send_keys(instructor1['wpi_id'])
    sleep(2)
    browser.find_element(By.NAME, "email").send_keys(instructor1['email'])
    sleep(2)
    browser.find_element(By.NAME, "phone").send_keys(instructor1['phone'])
    sleep(2)
    browser.find_element(By.NAME, "username").send_keys(instructor1['username'])
    sleep(2)
    browser.find_element(By.NAME, "password").send_keys(instructor1['password'])
    sleep(2)
    browser.find_element(By.NAME, "password2").send_keys(instructor1['password'])
    sleep(2)
    browser.find_element(By.NAME, "submit").click()
    sleep(2)
    #verification
    content = browser.page_source
    # print(content)
    assert 'Congratulations, you are now a registered instructor user!' in content

def test_register_student(browser,student1):

    browser.get('http://localhost:5000/student/studentregister')
    # Enable this to maximize the window
    browser.maximize_window()
    browser.find_element(By.NAME, "first_name").send_keys(student1['firstname'])
    sleep(2)
    browser.find_element(By.NAME, "last_name").send_keys(student1['lastname'])
    sleep(2)
    browser.find_element(By.NAME, "email").send_keys(student1['email'])
    sleep(2)
    browser.find_element(By.NAME, "wpi_id").send_keys(student1['wpi_id'])
    sleep(2)
    browser.find_element(By.NAME, "phone").send_keys(student1['phone'])
    sleep(2)
    browser.find_element(By.NAME, "username").send_keys(student1['username'])
    sleep(2)
    browser.find_element(By.NAME, "password").send_keys(student1['password'])
    sleep(2)
    browser.find_element(By.NAME, "password2").send_keys(student1['password'])
    sleep(2)
    browser.find_element(By.NAME, "GPA").send_keys(student1['gpa'])
    sleep(2)
    browser.find_element(By.NAME, "graduation_date").send_keys(student1['graduation_date'])
    sleep(2)
    browser.find_element(By.NAME, "courses-0-course").send_keys(student1['course'])
    #Select(browser.find_element(By.NAME, "courses-0-course")).select_by_visible_text(student1['course'])
    sleep(2)
    Select(browser.find_element(By.NAME, "courses-0-grade")).select_by_visible_text(student1['grade'])
    sleep(2)
    browser.find_element(By.NAME, "courses-0-sa_experience").click()
    sleep(2)
    browser.find_element(By.NAME, "submit").click()
    sleep(2)
    #verification
    content = browser.page_source
    # print(content)
    assert 'Congratulations, you are now a registered student user!' in content

def test_login_form(browser,instructor1):
    browser.get('http://localhost:5000/user/login')
    browser.maximize_window()
    browser.find_element(By.NAME, "username").send_keys(instructor1['username'])
    sleep(2)
    browser.find_element(By.NAME, "password").send_keys(instructor1['password'])
    sleep(2)
    browser.find_element(By.NAME, "remember_me").click()
    sleep(2)
    button = browser.find_element(By.NAME, "submit").click()
    sleep(2)
    #verification
    content = browser.page_source
    assert 'Welcome Instructor' in content
    assert instructor1['firstname'] in content

def test_create_coursection(browser, instructor1, coursection):
    browser.get('http://localhost:5000/user/login')
    browser.maximize_window()
    browser.find_element(By.NAME, "username").send_keys(instructor1['username'])
    browser.find_element(By.NAME, "password").send_keys(instructor1['password'])
    browser.find_element(By.NAME, "remember_me").click()
    browser.find_element(By.NAME, "submit").click()

    #browser.get('http://localhost:5000/instructor/create_course')
    sleep(2)
    browser.find_element(By.NAME, "create-course-section").click()
    sleep(2)
    browser.find_element(By.NAME, "course_number").send_keys(coursection['course_number'])
    sleep(2)
    browser.find_element(By.NAME, "section").send_keys(coursection['section'])
    sleep(2)
    browser.find_element(By.NAME, "year").send_keys(coursection['year'])
    sleep(2)
    Select(browser.find_element(By.NAME, "term")).select_by_visible_text(coursection['term'])
    sleep(2)
    browser.find_element(By.NAME, "submit").click()
    sleep(2)
    # verification
    content = browser.page_source
    assert coursection['course_number'] in content
    assert coursection['section'] in content
    assert coursection['year'] in content
    # assert coursection['term'] in content
    assert 'The new course has successfully posted!' in content

def test_create_position(browser, instructor1, coursection, position):
    browser.get('http://localhost:5000/user/login')
    browser.maximize_window()
    browser.find_element(By.NAME, "username").send_keys(instructor1['username'])
    browser.find_element(By.NAME, "password").send_keys(instructor1['password'])
    browser.find_element(By.NAME, "remember_me").click()
    browser.find_element(By.NAME, "submit").click()

    #cs = db.session.scalars(sqla.select(CourseSection).where(CourseSection.course_number == coursection['course_number']).where(CourseSection.section == coursection['section']).where(CourseSection.term == coursection['year']+'C')).first()
    sleep(2)
    #browser.find_element(By.ID, f"pos-btn-{cs.id}").click()
    browser.find_element(By.ID, f"pos-btn-{1}").click()
    sleep(2)
    #browser.get('http://localhost:5000/instructor/'+str(cs.id)+'/create_position')
    browser.find_element(By.NAME, "num_SAs").send_keys(position['num_SAs'])
    sleep(2)
    browser.find_element(By.NAME, "min_GPA").send_keys(position['min_GPA'])
    sleep(2)
    browser.find_element(By.NAME, "min_grade").send_keys(position['min_grade'])
    sleep(2)
    browser.find_element(By.NAME, "submit").click()
    sleep(2)
    content = browser.page_source
    assert 'The new position has been successfully added!' in content
    browser.find_element(By.ID, f"button-{1}").click()
    sleep(2)
    # content = browser.page_source
    # assert position['num_SAs'] in content
    # assert position['min_GPA'] in content
    # assert position['min_grade'] in content


def test_apply(browser, student1, coursection, apply):
    browser.get('http://localhost:5000/user/login')
    browser.maximize_window()
    browser.find_element(By.NAME, "username").send_keys(student1['username'])
    browser.find_element(By.NAME, "password").send_keys(student1['password'])
    browser.find_element(By.NAME, "remember_me").click()
    browser.find_element(By.NAME, "submit").click()

    # cs = db.session.scalars(
    #     sqla.select(CourseSection).where(CourseSection.course_number == coursection['course_number']).where(
    #         CourseSection.section == coursection['section']).where(CourseSection.term == coursection['term'])).first()
    sleep(2)
    #browser.find_element(By.ID, f"apply-btn-{cs.position.id}").click()
    browser.find_element(By.ID, f"apply-btn-{1}").click()
    sleep(2)

    #browser.get('http://localhost:5000/positions/'+str(cs.position.id)+'/apply')
    browser.find_element(By.NAME, "grade").send_keys(apply['grade'])
    sleep(2)
    browser.find_element(By.NAME, "year_taken").send_keys(apply['year_taken'])
    sleep(2)
    browser.find_element(By.NAME, "term_taken").send_keys(apply['term_taken'])
    sleep(2)
    browser.find_element(By.NAME, "submit").click()
    sleep(2)
    content = browser.page_source
    assert 'You have successfully applied for the course!' in content


def test_assign(browser, instructor1, coursection, position, student1):
    browser.get('http://localhost:5000/user/login')
    browser.maximize_window()
    browser.find_element(By.NAME, "username").send_keys(instructor1['username'])
    browser.find_element(By.NAME, "password").send_keys(instructor1['password'])
    browser.find_element(By.NAME, "remember_me").click()
    browser.find_element(By.NAME, "submit").click()

    # cs = db.session.scalars(
    #     sqla.select(CourseSection).where(CourseSection.course_number == coursection['course_number']).where(
    #         CourseSection.section == coursection['section']).where(CourseSection.term == coursection['term'])).first()

    # std = db.session.scalars(sqla.select(Student).where(Student.username == student1['username']).where(Student.email == student1['email'])).first()
    sleep(2)
    # browser.find_element(By.ID, f"view-applicants-{cs.position.id}").click()
    browser.find_element(By.ID, f"view-applicants-{1}").click()
    sleep(2)
    # browser.find_element(By.ID, f"accept-btn-${std.id}-${cs.position.id}").click()
    browser.find_element(By.ID, f"accept-btn-{4}-{1}").click()
    sleep(2)

    #browser.get('http://localhost:5000/position/'+str(cs.position.id)+'/'+str(std.id)+'/accept')
    content = browser.page_source
    assert 'Student successfully assigned to SA position' in content

def test_view_profile(browser, student1):
    browser.get('http://localhost:5000/user/login')
    browser.maximize_window()
    browser.find_element(By.NAME, "username").send_keys(student1['username'])
    browser.find_element(By.NAME, "password").send_keys(student1['password'])
    browser.find_element(By.NAME, "remember_me").click()
    browser.find_element(By.NAME, "submit").click()

    sleep(2)
    browser.find_element(By.NAME, "actions").click()
    sleep(2)
    browser.find_element(By.NAME, "std-prof").click()
    sleep(2)
    browser.find_element(By.NAME, "go-back").click()
    sleep(2)
    content = browser.page_source
    assert 'Welcome Student -' in content
    assert student1['firstname'] in content


if __name__ == "__main__":
    retcode = pytest.main(verbose=2)
