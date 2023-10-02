from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
import os

db = SQLAlchemy()
DB_NAME = "database.db"
mail = Mail()

def CreateApp():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECURITY_PASSWORD_SALT"] = os.getenv("SECURITY_PASSWORD_SALT")
    db.init_app(app)
    migrate = Migrate(app, db)

    from .auth.auth import auth
    from .mh.mh import mh

    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(mh, url_prefix="/mh")

    from .models import User
    login_manager = LoginManager()
    login_manager.login_view = "auth.Login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    CreateDatabase(app)
    
    # Set up Flask Mail settings
    app.config.update(dict(
        DEBUG = False,
        MAIL_SERVER = "smtp.gmail.com",
        MAIL_PORT = 587,
        MAIL_USE_TLS = True,
        MAIL_USE_SSL = False,
        MAIL_USERNAME = os.getenv("EMAIL"),
        MAIL_PASSWORD = os.getenv("APP_PASSWORD"),
    ))
    mail = Mail(app)

    return app

def CreateDatabase(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print("Created database!")


def GetNotifications():
    # try:
    return dict(n_help=0, n_edit=0, n_report=0, n_request=0, n_notifications=0)