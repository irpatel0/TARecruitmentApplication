from config import Config

from app import create_app, db
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo
from app.main.models import User, Student, Instructor, Course

app = create_app(Config)

@app.shell_context_processor
def make_shell_context():
    return {'sqla': sqla, 'sqlo': sqlo, 'db': db, 'User': User, 'Student': Student, 'Instructor': Instructor}

def add_classes(*args, **kwargs):
    query = sqla.select(Course)
    if db.session.scalars(query).first() is None:
        courses = ['CS1001','CS2002', 'CS3003', 'CS4004']
        titles = ['Intro to CS', 'Data Structures', 'Algorithms', 'Software Engineering']
        for i in range (len(courses)):
            db.session.add(Course(number=courses[i], title=titles[i]))
        db.session.commit()


@app.before_request
def initDB(*args, **kwargs):
    if app._got_first_request:
        db.create_all()
        add_classes()


if __name__ == "__main__":
    app.run(debug=True)