from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()

migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.static_folder = config_class.STATIC_FOLDER
    app.template_folder = config_class.TEMPLATE_FOLDER_MAIN

    db.init_app(app)
    migrate.init_app(app, db)

    # blueprint registration
    from app.main import main_blueprint as main
    main.template_folder = Config.TEMPLATE_FOLDER_MAIN
    app.register_blueprint(main)

    from app.auth import auth_blueprint as auth
    auth.template_folder = Config.TEMPLATE_FOLDER_AUTH
    app.register_blueprint(auth)

    from app.errors import error_blueprint as errors
    errors.template_folder = Config.TEMPLATE_FOLDER_ERRORS
    app.register_blueprint(errors)

    from app.student import student_blueprint as student
    student.template_folder = Config.TEMPLATE_FOLDER_STUDENT
    app.register_blueprint(student)

    from app.instructor import instructor_blueprint as instructor
    instructor.template_folder = Config.TEMPLATE_FOLDER_INSTRUCTOR
    app.register_blueprint(instructor)

    return app
