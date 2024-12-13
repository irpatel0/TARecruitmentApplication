from config import Config

from app import create_app, db
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo
from app.main.models import User, Student, Instructor, Course, Application, Position, CourseSection, CourseTaken
from werkzeug.middleware.proxy_fix import ProxyFix
import identity.web


app = create_app(Config)

app.jinja_env.globals.update(Auth=identity.web.Auth)  # Useful in template for B2C
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

@app.shell_context_processor
def make_shell_context():
    return {'sqla': sqla, 'sqlo': sqlo, 'db': db, 'User': User, 'Student': Student, 'Instructor': Instructor,
            'Course': Course, 'Application': Application, 'Position': Position, 'CourseSection': CourseSection, 'CourseTaken': CourseTaken}

def add_classes(*args, **kwargs):
    query = sqla.select(Course)
    if db.session.scalars(query).first() is None:
        courses = ['CS1101', 'CS2102', 'CS2223', 'CS2303', 'CS3013', 'CS3133', 'CS3431', 'CS3733', 'CS4341', 'CS4241', 'CS4342', 'CS4433']
        titles = ['Introduction To Program Design', 'Object-Oriented Design Concepts', 'Algorithms', 'Systems Programming Concepts', 'Operating Systems', 'Foundations Of Computer Science', 'Database Systems I', 'Software Engineering', 'Introduction To Artificial Intelligence', 'Webware: Computational Technology For Network Information Systems', 'Machine Learning', 'Big Data Management and Analytics']
        for i in range (len(courses)):
            db.session.add(Course(number=courses[i], title=titles[i]))
        db.session.commit()

#Adds Insturctor with username: teacher and password: 123
#Adds Student with username: student and password: 123
def add_users(*args, **kwargs):
    query = sqla.select(User)
    if db.session.scalars(query).first() is None:
        instructor = Instructor(username = "teacher",
                            firstname = "John",
                            lastname = "Doe",
                            wpi_id = "123123123",
                            email = "teacher@wpi.edu",
                            phone = "1234567890",
                            user_type = "Instructor")
        instructor.set_password("123")
        student = Student(username = "student",
                            firstname = "Little",
                            lastname = "Bob",
                            wpi_id = "321321321",
                            email = "student@wpi.edu",
                            phone = "0987654321",
                            user_type = "Student",
                            gpa = 4.0,
                            graduation_date = "2025")
        student.set_password("123")
        db.session.add(instructor)
        db.session.add(student)
        db.session.commit()

@app.before_request
def initDB(*args, **kwargs):
    if app._got_first_request:
        db.create_all()
        #add_classes()
        add_classes(*args, **kwargs) 
        add_users(*args, **kwargs)


if __name__ == "__main__":
    app.run(debug=True)