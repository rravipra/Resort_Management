from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS

import yaml

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    # bcrypt = Bcrypt(app)
    db_creds = yaml.load(open('./flask_crud/database.yaml'))
    app.config['MYSQL_HOST'] = db_creds['host']
    app.config['MYSQL_USER'] = db_creds['user']
    app.config['MYSQL_PASSWORD'] = db_creds['pass']
    app.config['MYSQL_DB'] = db_creds['db']
    app.config['SECRET_KEY'] = "rthishot"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://flask:flask@localhost/resort_management'

    db.init_app(app)

    from .models import Employee, Guest, Room

    cors = CORS(app, resources={r"*": {"origins": "*"}})

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(user_id):
        return Employee.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app