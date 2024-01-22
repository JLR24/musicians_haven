from ... import db, mail
from ...models import User, UserSetting
from flask_login import current_user
from flask_mail import Message
from flask import flash, current_app, session, render_template, redirect, url_for, request
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash
from werkzeug.urls import url_parse
from os import getenv


def is_logged_in():
    '''Returns True if the user is logged in, False otherwise'''
    if current_user.is_authenticated:
        flash("You are already logged in!", category="error")
        return True
    return False


def get_user(key):
    '''Returns the user object from a key, either their username or email, None otherwise'''
    user = User.query.filter_by(username=key).first()
    if not user:
        return User.query.filter_by(email=key).first()
    return user


def check_user(username, email):
    '''Returns True if the username and email are safe to use, False otherwise'''
    if get_user(username) or get_user(email) or len(username) < 1:
        return False
    return True


def generate_token():
    '''Generates and returns the validation token to be emailed'''
    s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return s.dumps(session["email"], salt=current_app.config["SECURITY_PASSWORD_SALT"])


def send_signup_token(token):
    '''Sends the email with the signup token'''
    try:
        # Define email details
        msg = Message("Musician's Haven Signup Code",
            sender = ("Musician's Haven", getenv("EMAIL")),
            recipients = [(str(session["email"]))]
        )
        msg.body = f"Your email address was used to sign up to Musician's Haven, please use this link to activate your account: http://127.0.0.1:5000/auth/validate/{token}"
        msg.html = render_template("email_signup.html", token=token, username=session["username"])
        mail.send(msg)
    except Exception as e:
        # If the process fails (most likely an account login failure)...
        flash(f'Mail send failure - - "{str(e)}" - - Please try again...', category="error")
        return redirect(url_for("auth.Signup"))
    

def check_token(token, expiration=600):
    '''Checks that the token is valid'''
    # Source: https://realpython.com/handling-email-confirmation-in-flask/
    serialiser = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        return serialiser.loads(token, salt=current_app.config["SECURITY_PASSWORD_SALT"], max_age=expiration)
    except:
        return False
    

def add_user():
    '''Creates new User and UserSetting objects to be added to the database, returns the User object'''
    db.session.add(User(
        username = session["username"],
        email = session["email"],
        password = generate_password_hash(session["pw"], method="sha256"),
        editor_score = 0,
        status = "User"
    ))
    db.session.commit()

    user = get_user(session["username"])
    if not user:
        session.clear()
        flash("Encountered an unknown error, please try again.", category="error")
        return redirect(url_for("auth.Signup"))
    
    db.session.add(UserSetting(
        user = user.id,
        messaging = "Anyone can message me",
        account_type = "Private",
        notifications = "11111111"
    ))
    db.session.commit()
    return user
    

def get_redirect_address():
    '''If the logged-out user is redirected to login, return to their previous page'''
    args = request.form.get("next")
    if not args or url_parse(args).netloc != "":
        args = url_for("mh.Home") # As a default, if no valid arguments are present
    return args