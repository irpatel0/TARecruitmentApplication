from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo
from flask_login import UserMixin
from app import login

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

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
    # TODO: courses taught
    graduation_date : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(4))

    __mapper_args__ = {'polymorphic_identity': 'Student'}

class Instructor(User):
    __tablename__ = 'instructor'
    id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(User.id), primary_key=True)

    __mapper_args__ = {'polymorphic_identity': 'Instructor'}