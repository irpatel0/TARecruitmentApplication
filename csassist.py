from config import Config

from app import create_app, db
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo
from app.main.models import User, Student, Instructor

app = create_app(Config)

@app.shell_context_processor
def make_shell_context():
    return {'sqla': sqla, 'sqlo': sqlo, 'db': db, 'User': User, 'Student': Student, 'Instructor': Instructor}

@app.before_request
def initDB(*args, **kwargs):
    if app._got_first_request:
        db.create_all()


if __name__ == "__main__":
    app.run(debug=True)