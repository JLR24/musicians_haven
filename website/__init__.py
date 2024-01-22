from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_mail import Mail
import os

db = SQLAlchemy()
DB_NAME = "database.db"
mail = Mail()

def create_app():
    # Initialise Flask app details
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECURITY_PASSWORD_SALT"] = os.getenv("SECURITY_PASSWORD_SALT")
    db.init_app(app)
    migrate = Migrate(app, db)

    # Import and register blueprints
    from .auth.auth import auth
    from .admin.admin import admin
    from .help.help import help
    from .mh.mh import mh
    from .mh.profile.profile import profile

    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(admin, url_prefix="/admin")
    app.register_blueprint(help, url_prefix="/help")
    app.register_blueprint(mh, url_prefix="/mh")
    app.register_blueprint(profile, url_prefix="/mh/profile")

    # Setup login manager
    from .models import User
    login_manager = LoginManager()
    login_manager.login_view = "auth.Login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    

    create_database(app)
    
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

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print("Created database!")


def get_notifications():
    '''Return a dict containing the user's notifications to be displayed as badge notifications on the site's navbar'''
    try:
        reports = 0
        edits = 0
        help = 0
        if current_user.status == "Admin":
            from .models import Help, Thread, ThreadPost, UserPost, Song, Album, SongContent
            reports = len(Song.query.filter_by(state="r").all()) + len(Thread.query.filter_by(state="r").all()) + len(ThreadPost.query.filter_by(state="r").all()) + len(SongContent.query.filter_by(state="r").all()) + len(UserPost.query.filter_by(state="r").all())
            edits = 0 # NOTE: PENDING
            help = len(Help.query.all())
        return dict(n_help = help, n_edit = edits, n_report = reports, n_notification = len(current_user.getNotifications(seen=False)))
    except:
        return dict(n_help=0, n_edit=0, n_report=0, n_notification=0)